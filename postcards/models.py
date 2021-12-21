import datetime

import requests
from django.db import models
from django.utils import timezone
from postcard_creator.postcard_creator import Token, PostcardCreator

from config import settings
from users.models import CustomUser


class PostcardCreatorCredentials(models.Model):
    access_token = models.CharField(null=True, blank=True, max_length=2048)
    refresh_token = models.CharField(null=True, blank=True, max_length=2048)
    expires_at = models.DateTimeField(null=True, blank=True)
    refreshed_at = models.DateTimeField(null=True, blank=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='credentials')

    def __str__(self):
        return "%s | %s" % (self.user.__str__(), self.expires_at)

    def get_token(self):
        token = Token()
        token.token = self.access_token
        token.token_implementation = 'swissid'

        return token

    def refresh(self):
        request_data = {
            'grant_type': 'refresh_token',
            'client_id': settings.PCC_CLIENT_ID,
            'client_secret': settings.PCC_CLIENT_SECRET,
            'refresh_token': self.refresh_token,
        }
        url = 'https://pccweb.api.post.ch/OAuth/token'
        resp = requests.post(url,
                             data=request_data,
                             headers=settings.PCC_HEADERS,
                             allow_redirects=False)

        if 'access_token' not in resp.json() or resp.status_code != 200:
            raise Exception("not able to fetch access token: " + resp.text)

        resp_json = resp.json()
        self.access_token = resp_json['access_token']
        self.refresh_token = resp_json['refresh_token']
        self.expires_at = timezone.now() + datetime.timedelta(seconds=resp_json['expires_in'])
        self.refreshed_at = timezone.now()
        self.save()

    def has_free_postcard(self):
        token = self.get_token()
        postcard_creator = PostcardCreator(token)
        return postcard_creator.has_free_postcard()
