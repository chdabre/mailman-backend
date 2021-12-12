from rest_framework import viewsets, serializers, mixins

from jobs.models import PostcardJob
from jobs.serializers import PostcardJobSerializer


class PostcardJobViewset(
            mixins.ListModelMixin,
            mixins.CreateModelMixin,
            mixins.DestroyModelMixin,
            viewsets.GenericViewSet
        ):
    serializer_class = PostcardJobSerializer
    queryset = PostcardJob.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)