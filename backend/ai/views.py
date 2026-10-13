
# """
# backend/ai/views.py

# The view only orchestrates: validate -> get AI extraction (cached) -> compare -> respond.
# It knows nothing about Gemini internals; services.py raises AIServiceError instead.
# """
# import hashlib
# import logging

# from django.core.cache import cache
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from profiles.models import Skill

# from .serializers import JobAnalysisSerializer
# from .services import AIServiceError, analyze_job_description
# from .skills import compare_skills

# logger = logging.getLogger(__name__)

# CACHE_SECONDS = 60 * 60 * 24
# # Bump this when the AI schema/prompt changes so stale cache entries are ignored.
# CACHE_VERSION = "v1"


# def get_ai_analysis(job_description: str) -> dict:
#     """AI extraction is the same for every user, so cache it by job text."""
#     digest = hashlib.sha256(job_description.encode("utf-8")).hexdigest()
#     key = f"jd_analysis:{CACHE_VERSION}:{digest}"

#     cached = cache.get(key)
#     if cached is not None:
#         return cached

#     result = analyze_job_description(job_description)  # may raise AIServiceError
#     cache.set(key, result, CACHE_SECONDS)
#     return result


# class JobAnalysisView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = JobAnalysisSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         job_description = serializer.validated_data["job_description"].strip()

#         try:
#             ai_result = get_ai_analysis(job_description)
#         except AIServiceError as exc:
#             logger.warning("AI analysis failed for user=%s: %s", request.user.pk, exc)
#             return Response({"error": str(exc)}, status=exc.status)

#         # Skills the user has demonstrated through their projects.
#         user_skills = sorted(
#             Skill.objects.filter(projects__user=request.user)
#             .values_list("name", flat=True)
#             .distinct()
#         )

#         required_skills = ai_result.get("required_skills", [])
#         preferred_skills = ai_result.get("preferred_skills", [])

#         # Temporary debug line: repr() exposes invisible whitespace/unicode differences.
#         # Remove once you are confident in the matching.
#         logger.info("skills debug user=%r required=%r", user_skills, required_skills)

#         comparison = compare_skills(user_skills, required_skills, preferred_skills)

#         return Response(
#             {
#                 "job_title": ai_result.get("job_title", ""),
#                 "required_skills": required_skills,
#                 "preferred_skills": preferred_skills,
#                 "user_skills": user_skills,
#                 **comparison,  # matched_skills, missing_skills, preferred_*, match_percentage
#                 "recommendations": ai_result.get("recommendations", []),
#             }
#         )


        #  **************newversions**************

import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from profiles.models import Skill

from .exceptions import AIServiceError
from .serializers import JobAnalysisSerializer
from .services import analyze_job

logger = logging.getLogger(__name__)


def get_user_skill_names(user) -> list[str]:
    """Skills the user has demonstrated through their projects."""
    return sorted(
        Skill.objects.filter(projects__user=user)
        .values_list("name", flat=True)
        .distinct()
    )


class JobAnalysisView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "ai_analyze"  # rate defined in settings.py (Step 1c)

    def post(self, request):
        serializer = JobAnalysisSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job_description = serializer.validated_data["job_description"]

        user_skills = get_user_skill_names(request.user)

        try:
            result = analyze_job(job_description, user_skills)
        except AIServiceError as exc:
            logger.warning("AI analysis failed user=%s code=%s", request.user.pk, exc.code)
            return Response(
                {"error": exc.message, "code": exc.code},
                status=exc.status_code,
            )

        return Response({"user_skills": user_skills, **result})