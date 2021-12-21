import datetime

from django.db import models
from postcard_creator.postcard_creator import Postcard, Recipient, Sender

from users.models import CustomUser


class Address(models.Model):
    firstname = models.CharField(null=False, blank=False, max_length=50)
    lastname = models.CharField(null=False, blank=False, max_length=50)
    street = models.CharField(null=False, blank=False, max_length=50)
    city = models.CharField(null=False, blank=False, max_length=50)
    zipcode = models.CharField(null=False, blank=False, max_length=10)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False, related_name='addresses')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return "%s | %s" % (self.get_full_name(), self.city)

    def get_full_name(self):
        return "%s %s" % (self.firstname, self.lastname)

    def to_sender(self):
        return Sender(
            prename=self.firstname,
            lastname=self.lastname,
            street=self.street,
            zip_code=self.zipcode,
            place=self.city,
        )

    def to_recipient(self):
        return Recipient(
            prename=self.firstname,
            lastname=self.lastname,
            street=self.street,
            zip_code=self.zipcode,
            place=self.city,
        )


class PostcardJob(models.Model):
    class JobStatus(models.TextChoices):
        WAITING = 'WAITING', 'Waiting'
        SENT = 'SENT', 'Sent'

    status = models.CharField(choices=JobStatus.choices, default=JobStatus.WAITING, null=False, blank=False, max_length=20)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    sender = models.ForeignKey(Address, on_delete=models.PROTECT, null=False, blank=False, related_name='sender_jobs')
    recipient = models.ForeignKey(Address, on_delete=models.PROTECT, null=False, blank=False, related_name='recipient_jobs')

    send_on = models.DateField(default=datetime.date.today, editable=True, blank=False, null=False)
    time_sent = models.DateTimeField(blank=True, null=True)

    message = models.CharField(max_length=500, blank=True)
    front_image = models.ImageField(upload_to='raw_image/', blank=True)
    text_image = models.ImageField(upload_to='text_image/', blank=True)

    class Meta:
        ordering = ('-status', '-send_on', '-time_sent', )

    def __str__(self):
        return "%s | %s: %s" % (self.user, self.status, self.send_on)

    def to_postcard(self):
        return Postcard(
            sender=self.sender.to_sender(),
            recipient=self.recipient.to_recipient(),
            message=self.message,
            picture_stream=self.front_image.file
        )

    def handle(self):
        print(self)