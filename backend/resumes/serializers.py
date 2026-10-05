from rest_framework import serializers

from .models import Resume, ResumeVersion


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            "id",
            "title",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ResumeVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeVersion
        fields = [
            "id",
            "resume",
            "version_number",
            "content",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "resume",
            "version_number",
            "created_at",
        ]