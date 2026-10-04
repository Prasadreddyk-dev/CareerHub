from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ProfileViewSet,
    SkillViewSet,
    EducationViewSet,
    ProjectViewSet,
    CertificationViewSet,
)


router = DefaultRouter()

router.register("profile", ProfileViewSet, basename="profile")
router.register("skills", SkillViewSet, basename="skills")
router.register("education", EducationViewSet, basename="education")
router.register("projects", ProjectViewSet, basename="projects")
router.register(
    "certifications",
    CertificationViewSet,
    basename="certifications",
)


urlpatterns = [
    path("", include(router.urls)),
]