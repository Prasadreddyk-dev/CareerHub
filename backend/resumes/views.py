from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Resume, ResumeVersion
from .serializers import ResumeSerializer, ResumeVersionSerializer


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(
            user=self.request.user
        ).prefetch_related("versions")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["get", "post"],
        url_path="versions",
    )
    def versions(self, request, pk=None):
        resume = self.get_object()

        if request.method == "GET":
            versions = resume.versions.all()

            serializer = ResumeVersionSerializer(
                versions,
                many=True,
            )

            return Response(serializer.data)

        serializer = ResumeVersionSerializer(
            data=request.data
        )

        if serializer.is_valid():
            latest_version = resume.versions.order_by(
                "-version_number"
            ).first()

            next_version = (
                latest_version.version_number + 1
                if latest_version
                else 1
            )

            version = serializer.save(
                resume=resume,
                version_number=next_version,
            )

            return Response(
                ResumeVersionSerializer(version).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ResumeVersionViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeVersionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ResumeVersion.objects.filter(
            resume__user=self.request.user
        )