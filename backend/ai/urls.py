from django.urls import path
from .views import JobAnalysisView


urlpatterns = [
    path(
        "analyze-job/",
        JobAnalysisView.as_view(),
        name="analyze-job"
    ),
]