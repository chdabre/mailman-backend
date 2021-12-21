from rest_framework import viewsets, mixins

from postcards.models import PostcardCreatorCredentials
from postcards.serializers import PostcardCreatorCredentialsSerializer
from postcards.tasks import import_user_address


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

    def perform_create(self, serializer):
        credentials = serializer.save(user=self.request.user)
        import_user_address(credentials)
