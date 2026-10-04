from rest_framework import serializers

from .models import (
    Profile,
    Skill,
    Education,
    Project,
    Certification,
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "phone",
            "location",
            "bio",
            "github_url",
            "linkedin_url",
            "portfolio_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "id",
            "degree",
            "institution",
            "field_of_study",
            "start_date",
            "end_date",
        ]
        read_only_fields = ["id"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "github_url",
            "live_url",
            "technologies",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = [
            "id",
            "name",
            "issuer",
            "issue_date",
            "credential_url",
        ]
        read_only_fields = ["id"]