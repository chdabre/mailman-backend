from rest_framework import viewsets, serializers

from jobs.models import PostcardJob
from jobs.serializers import PostcardJobSerializer


class PostcardJobViewset(viewsets.ModelViewSet):
    serializer_class = PostcardJobSerializer
    queryset = PostcardJob.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)