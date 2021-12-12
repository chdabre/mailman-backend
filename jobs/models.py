import datetime

from django.db import models

from users.models import CustomUser


class PostcardJob(models.Model):
    class JobStatus(models.TextChoices):
        CREATED = 'CREATED', 'Created'
        WAITING = 'WAITING', 'Waiting'
        ENQUEUED = 'ENQUEUED', 'Enqueued'
        SENT = 'SENT', 'Sent'

    status = models.CharField(choices=JobStatus.choices, default=JobStatus.CREATED, null=False, blank=False, max_length=20)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    send_on = models.DateTimeField(default=datetime.datetime.now, blank=False, null=False)
    time_sent = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s | %s" % (self.user, self.status)