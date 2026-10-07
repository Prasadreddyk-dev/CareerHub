from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application

        fields = [
            "id",
            "job",
            "resume",
            "status",
            "applied_at",
            "notes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "applied_at",
            "created_at",
            "updated_at",
        ]