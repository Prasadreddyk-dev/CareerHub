from django.conf import settings
from django.db import models


class Application(models.Model):

    class Status(models.TextChoices):
        SAVED = "SAVED", "Saved"
        APPLIED = "APPLIED", "Applied"
        ASSESSMENT = "ASSESSMENT", "Assessment"
        TECHNICAL_INTERVIEW = (
            "TECHNICAL_INTERVIEW",
            "Technical Interview",
        )
        HR_INTERVIEW = "HR_INTERVIEW", "HR Interview"
        OFFER = "OFFER", "Offer"
        REJECTED = "REJECTED", "Rejected"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    job = models.ForeignKey(
        "jobs.Job",
        on_delete=models.CASCADE,
        related_name="applications",
    )

    resume = models.ForeignKey(
        "resumes.Resume",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="applications",
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.SAVED,
    )

    applied_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "job"],
                name="unique_user_job_application",
            )
        ]
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.user.email} - {self.job.title}"
