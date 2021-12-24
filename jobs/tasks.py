import os
import shutil
from datetime import datetime
from time import strftime, gmtime

from celery import shared_task
from django.core.files import File
from django.utils import timezone
from firebase_admin._messaging_encoder import Message
from firebase_admin._messaging_utils import Notification
from postcard_creator.postcard_creator import PostcardCreator

from config import settings
from jobs.models import PostcardJob
from users.models import CustomUser
from users.tasks import send_push_notification


@shared_task
def render_preview(job):
    credentials = job.user.credentials.first()

    postcard_creator = PostcardCreator(credentials.get_token())
    postcard_creator.send_free_card(
        postcard=job.to_postcard(),
        mock_send=True,
        image_export=True
    )

    try:
        trace_dir = os.path.join(os.getcwd(), '.postcard_creator_wrapper_sent')
        files = os.listdir(trace_dir)
        text_image_filename = next(f for f in files if '_text.jpg' in f)
        path = os.path.join(trace_dir, text_image_filename)

        job.text_image.save(text_image_filename, File(open(path, 'rb')))
        shutil.rmtree(trace_dir)
    except:
        pass

    job.save()


@shared_task
def send_postcard(job):
    print("Sending postcard: %s" % (job))
    credentials = job.user.credentials.first()

    postcard_creator = PostcardCreator(credentials.get_token())
    postcard_creator.send_free_card(
        postcard=job.to_postcard(),
        mock_send=settings.DEBUG,
        image_export=True
    )

    try:
        trace_dir = os.path.join(os.getcwd(), '.postcard_creator_wrapper_sent')
        files = os.listdir(trace_dir)
        text_image_filename = next(f for f in files if '_text.jpg' in f)
        path = os.path.join(trace_dir, text_image_filename)

        job.text_image.save(text_image_filename, File(open(path, 'rb')))
        shutil.rmtree(trace_dir)
    except:
        pass

    job.status = PostcardJob.JobStatus.SENT
    job.time_sent = timezone.now()
    job.save()

    sent_notification = Message(
        notification=Notification(
            title="Postcard sent",
            body="Your Postcard has been sent successfully!",
            image=job.front_image.url,
        )
    )
    send_push_notification(job.user, sent_notification)


@shared_task()
def handle_jobs():
    print("Handle jobs")
    users = CustomUser.objects.all()
    for user in users:
        print("Handle user id %d | %s" % (user.id, user))
        waiting_jobs = PostcardJob.objects.filter(user=user, status=PostcardJob.JobStatus.WAITING).order_by('send_on')

        if waiting_jobs.count() > 0:
            credentials = user.credentials.first()
            if credentials:
                credentials.refresh()

                if credentials.has_free_postcard() or settings.DEBUG:
                    job = waiting_jobs.filter(send_on=timezone.now()).first()
                    if job:
                        print("Job with send_on date found: %s" % (job))
                    else:
                        job = waiting_jobs.first()
                        print("No prioritized jobs, taking oldest in queue: %s" % (job))

                    send_postcard(job)
                else:
                    print("No free postcard available for this user.")
            else:
                print("User has no credentials")
        else:
            print("User has no waiting jobs")
