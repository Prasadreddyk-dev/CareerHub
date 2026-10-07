from django.utils import timezone
from rest_framework import filters, status, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Application
from .serializers import ApplicationSerializer


STATUS_TRANSITIONS = {
    "SAVED": {
        "APPLIED",
    },

    "APPLIED": {
        "ASSESSMENT",
        "TECHNICAL_INTERVIEW",
        "REJECTED",
    },

    "ASSESSMENT": {
        "TECHNICAL_INTERVIEW",
        "REJECTED",
    },

    "TECHNICAL_INTERVIEW": {
        "HR_INTERVIEW",
        "REJECTED",
    },

    "HR_INTERVIEW": {
        "OFFER",
        "REJECTED",
    },

    "OFFER": set(),

    "REJECTED": set(),
}


class ApplicationViewSet(viewsets.ModelViewSet):

    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
    DjangoFilterBackend,
    filters.OrderingFilter]

    filterset_fields = [
        "status",
        "job",
        "resume",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "applied_at",
    ]

    ordering = [
        "-updated_at"
    ]



    

    def get_queryset(self):
        return Application.objects.filter(
            user=self.request.user
        ).select_related(
            "job",
            "resume",
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="status",
    )
    def update_status(self, request, pk=None):

        application = self.get_object()

        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {
                    "error": "status is required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_statuses = {
            choice[0]
            for choice in Application.Status.choices
        }

        if new_status not in valid_statuses:
            return Response(
                {
                    "error": "Invalid status",
                    "allowed_statuses": list(
                        valid_statuses
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_status = application.status

        allowed_next_statuses = STATUS_TRANSITIONS.get(
            current_status,
            set(),
        )

        if new_status not in allowed_next_statuses:
            return Response(
                {
                    "error": (
                        f"Cannot move application from "
                        f"{current_status} to {new_status}"
                    ),
                    "allowed_next_statuses": list(
                        allowed_next_statuses
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        application.status = new_status

        if (
            new_status == Application.Status.APPLIED
            and application.applied_at is None
        ):
            application.applied_at = timezone.now()

        application.save()

        return Response(
            ApplicationSerializer(application).data
        )