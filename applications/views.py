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


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def withdraw_application(request, application_id):
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return Response(
            {"error": f"There is no application with id {application_id}"},
            status=status.HTTP_404_NOT_FOUND
        )

    if application.user != request.user:
        return Response(
            {"error": "You cannot withdraw an application that is not yours"},
            status=status.HTTP_403_FORBIDDEN
        )

    application.delete()
    return Response(
        {"message": f"Application with id {application_id} has been withdrawn"},
        status=status.HTTP_204_NO_CONTENT
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_applications(request):
    applications = Application.objects.filter(applicant=request.user)
    serializer = ApplicationSerializer(applications, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)