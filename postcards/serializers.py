from rest_framework import serializers

from postcards.models import PostcardCreatorCredentials


class PostcardCreatorCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostcardCreatorCredentials
        fields = ['id', 'access_token', 'refresh_token', 'expires_at', 'refreshed_at']