from rest_framework import serializers

from jobs.models import PostcardJob


class PostcardJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostcardJob
        fields = ['id', 'status', 'send_on', 'time_sent']