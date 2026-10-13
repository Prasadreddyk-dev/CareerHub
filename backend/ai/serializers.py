# from rest_framework import serializers


# class JobAnalysisSerializer(serializers.Serializer):

#     job_description = serializers.CharField(
#         required=True,
#         allow_blank=False
#     )

from rest_framework import serializers


class JobAnalysisSerializer(serializers.Serializer):
    job_description = serializers.CharField(
        required=True,
        allow_blank=False,
        min_length=30,
        max_length=8000,
    )