from django.db.models import Count
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from jobs.models import PostcardJob, Address
from jobs.serializers import PostcardJobSerializer, AddressSerializer
from jobs.tasks import render_preview


class PostcardJobViewset(
            mixins.ListModelMixin,
            mixins.CreateModelMixin,
            mixins.UpdateModelMixin,
            mixins.DestroyModelMixin,
            viewsets.GenericViewSet
        ):
    serializer_class = PostcardJobSerializer
    queryset = PostcardJob.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        job = serializer.save(user=self.request.user)
        print(job.text_image)
        if not job.text_image:
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
        return queryset.filter(user=self.request.user, display_status=Address.AddressDisplayStatus.ACTIVE)\
                .annotate(num_used=Count('recipient_jobs'))\
                .order_by('-is_primary', '-num_used')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.display_status = Address.AddressDisplayStatus.DELETED
        instance.save()

    @action(detail=True, methods=['post'], serializer_class=None)
    def set_primary(self, request, *args, **kwargs):
        address = self.get_object()
        user = address.user
        user.addresses.all().update(is_primary=False)

        address.is_primary = True
        address.save()

        serializer = AddressSerializer(address)
        return Response(serializer.data)
