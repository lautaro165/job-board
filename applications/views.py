from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework import status, generics

from jobs.models import JobPost
from .models import Application
from .serializers import ApplicationSerializer, ApplicationResponseSerializer

# Create your views here.

class ApplyToJobView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_job(self):
        job_id = self.kwargs.get("job_id")
        return JobPost.objects.get(id=job_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        context["job"] = self.get_job()
        return context

    def perform_create(self, serializer):
        job = self.get_job()
        if Application.objects.filter(applicant=self.request.user, job=job).exists():
            raise ValidationError("You have already applied to this job.")
        serializer.save(applicant=self.request.user, job=job)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def responde_to_application(request, application_id):
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return Response({"error": f"There is no application with id {application_id}"},status=status.HTTP_404_NOT_FOUND)

    if request.user != application.job.owner:
        return Response({"error":"You can't access to handle this application"}, status=status.HTTP_403_FORBIDDEN)
    
    status_value = request.data.get("status")
    message = request.data.get("message")

    if not status_value in ["accepted", "rejected", "reviewed"]:
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

    response_serializer = ApplicationResponseSerializer(data={
        "application":application.id,
        "responder":request.user.id,
        "message":message
    })

    application.status = status_value
    application.save()

    if response_serializer.is_valid():
        response_serializer.save()
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_job_applications(request, job_id):
    try:
        job = JobPost.objects.get(id=job_id)
    except JobPost.DoesNotExist:
        return Response({"error":f"No job found with id {job_id}"}, status=status.HTTP_404_NOT_FOUND)
    
    if job.owner != request.user:
        return Response({"error":"You can't access to this job's applications"},status=status.HTTP_403_FORBIDDEN)

    applications = Application.objects.filter(job=job)
    serializer = ApplicationSerializer(applications, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)