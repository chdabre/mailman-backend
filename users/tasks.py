from celery import shared_task
from fcm_django.models import FCMDevice


@shared_task
def send_push_notification(user, notification):
    user_devices = FCMDevice.objects.filter(user=user)
    user_devices.send_message(notification)