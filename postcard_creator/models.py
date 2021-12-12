from django.db import models

from users.models import CustomUser


class PostcardCreatorCredentials(models.Model):
    access_token = models.CharField(null=True, blank=True, max_length=2048)
    refresh_token = models.CharField(null=True, blank=True, max_length=2048)
    expires_at = models.DateTimeField(null=True, blank=True)
    refreshed_at = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='credentials')

    def __str__(self):
        return "%s | %s" % (self.user.__str__(), self.expires_at)