from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def HealthCheck(request):
    return Response({
        "status": "success",
        "message": "CareerHub API is running"
    })