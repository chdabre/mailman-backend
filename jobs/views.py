from rest_framework import viewsets, mixins

from jobs.models import PostcardJob, Address
from jobs.serializers import PostcardJobSerializer, AddressSerializer
from jobs.tasks import render_preview


class PostcardJobViewset(
            mixins.ListModelMixin,
            mixins.CreateModelMixin,
            mixins.DestroyModelMixin,
            viewsets.GenericViewSet
        ):
    serializer_class = PostcardJobSerializer
    queryset = PostcardJob.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        job = serializer.save(user=self.request.user)
        render_preview(job)


class AddressViewset(
            mixins.ListModelMixin,
            mixins.CreateModelMixin,
            mixins.DestroyModelMixin,
            viewsets.GenericViewSet
        ):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)