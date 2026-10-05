from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ResumeViewSet, ResumeVersionViewSet


router = DefaultRouter()

router.register('resumes', ResumeViewSet, basename="resume")

router.register("versions", ResumeVersionViewSet, basename="resume-version")



urlpatterns = [

    path("", include(router.urls)),
]