from rest_framework import viewsets, mixins

from postcard_creator.models import PostcardCreatorCredentials
from postcard_creator.serializers import PostcardCreatorCredentialsSerializer


class PostcardCreatorCredentialsViewSet(
            mixins.ListModelMixin,
            mixins.CreateModelMixin,
            mixins.RetrieveModelMixin,
            mixins.DestroyModelMixin,
            viewsets.GenericViewSet
        ):
    serializer_class = PostcardCreatorCredentialsSerializer
    queryset = PostcardCreatorCredentials.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)
