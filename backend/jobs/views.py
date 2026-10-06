from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .models import Job
from .serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):

    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "location",
        "employment_type",
        "company",
    ]

    search_fields = [
        "title",
        "company",
        "description",
        "location",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "title",
        "company",
        "application_deadline",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        return Job.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )