from rest_framework import viewsets

from postcard_creator.models import PostcardCreatorCredentials
from postcard_creator.serializers import PostcardCreatorCredentialsSerializer


class PostcardCreatorCredentialsViewSet(viewsets.ModelViewSet):
    serializer_class = PostcardCreatorCredentialsSerializer
    queryset = PostcardCreatorCredentials.objects.all()