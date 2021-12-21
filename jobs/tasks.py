import os
import shutil
from datetime import datetime
from time import strftime, gmtime

from celery import shared_task
from django.core.files import File
from django.utils import timezone
from postcard_creator.postcard_creator import PostcardCreator

from config import settings
from jobs.models import PostcardJob
from users.models import CustomUser


@shared_task
def render_preview(job):
    credentials = job.user.credentials.first()

    postcard_creator = PostcardCreator(credentials.get_token())
    postcard_creator.send_free_card(
        postcard=job.to_postcard(),
        mock_send=True,
        image_export=True
    )

    trace_dir = os.path.join(os.getcwd(), '.postcard_creator_wrapper_sent')
    file_name = strftime("postcard_creator_export_%Y-%m-%d_%H-%M-%S_text.jpg", gmtime())
    path = os.path.join(trace_dir, file_name)

    job.text_image.save(file_name, File(open(path, 'rb')))
    job.save()

    shutil.rmtree(trace_dir)


@shared_task
def send_postcard(job):
    print("Sending postcard: %s" % (job))
    credentials = job.user.credentials.first()

    postcard_creator = PostcardCreator(credentials.get_token())
    postcard_creator.send_free_card(
        postcard=job.to_postcard(),
        mock_send=True, #settings.DEBUG,
        image_export=True
    )

    trace_dir = os.path.join(os.getcwd(), '.postcard_creator_wrapper_sent')
    file_name = strftime("postcard_creator_export_%Y-%m-%d_%H-%M-%S_text.jpg", gmtime())
    path = os.path.join(trace_dir, file_name)

    job.text_image.save(file_name, File(open(path, 'rb')))
    job.status = PostcardJob.JobStatus.SENT
    job.time_sent = timezone.now()
    job.save()

    shutil.rmtree(trace_dir)


@shared_task()
def handle_jobs():
    print("Handle jobs")
    users = CustomUser.objects.all()
    for user in users:
        print("Handle user id %d | %s" % (user.id, user))
        waiting_jobs = PostcardJob.objects.filter(status=PostcardJob.JobStatus.WAITING).order_by('send_on')

        if waiting_jobs.count() > 0:
            credentials = user.credentials.first()
            if credentials:
                credentials.refresh()

                if credentials.has_free_postcard():
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
