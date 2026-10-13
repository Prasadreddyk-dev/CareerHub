from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from jobs.models import Job
from resumes.models import Resume
from applications.models import Application


class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        # -----------------------------
        # Summary
        # -----------------------------

        total_jobs = Job.objects.filter(
            user=user
        ).count()

        total_applications = Application.objects.filter(
            user=user
        ).count()

        total_resumes = Resume.objects.filter(
            user=user
        ).count()

        # -----------------------------
        # Applications by status
        # -----------------------------

        status_data = Application.objects.filter(
            user=user
        ).values(
            "status"
        ).annotate(
            total=Count("id")
        )

        applications_by_status = {
            item["status"]: item["total"]
            for item in status_data
        }

        # -----------------------------
        # Application metrics
        # -----------------------------

        interview_count = Application.objects.filter(
            user=user
        ).filter(
            Q(status=Application.Status.TECHNICAL_INTERVIEW)
            | Q(status=Application.Status.HR_INTERVIEW)
        ).count()

        offer_count = Application.objects.filter(
            user=user,
            status=Application.Status.OFFER
        ).count()

        rejected_count = Application.objects.filter(
            user=user,
            status=Application.Status.REJECTED
        ).count()

        # -----------------------------
        # Recent applications
        # -----------------------------

        recent_applications = Application.objects.filter(
            user=user
        ).select_related(
            "job",
            "resume"
        ).order_by(
            "-created_at"
        )[:5]

        recent_data = []

        for application in recent_applications:
            recent_data.append({
                "id": application.id,
                "job": {
                    "title": application.job.title,
                    "company": application.job.company,
                },
                "status": application.status,
                "applied_at": application.applied_at,
            })

        # -----------------------------
        # Final response
        # -----------------------------

        return Response({
            "summary": {
                "total_jobs": total_jobs,
                "total_applications": total_applications,
                "total_resumes": total_resumes,
            },

            "applications_by_status": applications_by_status,

            "metrics": {
                "interviews": interview_count,
                "offers": offer_count,
                "rejected": rejected_count,
            },

            "recent_applications": recent_data,
        })


