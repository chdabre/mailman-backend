import datetime

from django.db import models

from users.models import CustomUser


class Address(models.Model):
    firstname = models.CharField(null=False, blank=False, max_length=50)
    lastname = models.CharField(null=False, blank=False, max_length=50)
    street = models.CharField(null=False, blank=False, max_length=50)
    city = models.CharField(null=False, blank=False, max_length=50)
    zipcode = models.CharField(null=False, blank=False, max_length=10)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return "%s | %s" % (self.get_full_name(), self.city)

    def get_full_name(self):
        return "%s %s" % (self.firstname, self.lastname)


class PostcardJob(models.Model):
    class JobStatus(models.TextChoices):
        CREATED = 'CREATED', 'Created'
        WAITING = 'WAITING', 'Waiting'
        ENQUEUED = 'ENQUEUED', 'Enqueued'
        SENT = 'SENT', 'Sent'

    status = models.CharField(choices=JobStatus.choices, default=JobStatus.CREATED, null=False, blank=False, max_length=20)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    sender = models.ForeignKey(Address, on_delete=models.PROTECT, null=False, blank=False, related_name='sender_jobs')
    recipient = models.ForeignKey(Address, on_delete=models.PROTECT, null=False, blank=False, related_name='recipient_jobs')

    send_on = models.DateTimeField(default=datetime.datetime.now, blank=False, null=False)
    time_sent = models.DateTimeField(blank=True, null=True)

    message = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return "%s | %s" % (self.user, self.status)
