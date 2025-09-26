from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from jobs.models import JobPost
from .models import Application
from .serializers import ApplicationSerializer

# Create your views here.

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def apply_to_job(request, job_id):
    try:
        job = JobPost.objects.get(id=job_id)
    except JobPost.DoesNotExist:
        return Response({"error": f"No job found with id {job_id}"}, status=status.HTTP_404_NOT_FOUND)
    
    if Application.objects.filter(applicant=request.user, job=job).exists():
        return Response(
            {"error": "You have already applied to this job."},
            status=status.HTTP_400_BAD_REQUEST
        )

    data = request.data.copy()
    
    serializer = ApplicationSerializer(data=data, context={"user": request.user, "job":job})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
