from django.shortcuts import get_object_or_404

from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework import status, generics

from jobs.models import JobPost
from jobs.permissions import IsJobOwner
from .exceptions import ForbiddenApplicationStatusUpdate
from .models import Application
from .serializers import ApplicationSerializer, ApplicationResponseSerializer, ApplicationStatusUpdateSerializer
from .services import apply_to_job_service, respond_to_application_service, withdraw_application_service


# Create your views here.

class ApplyToJobView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_job(self):
        job_id = self.kwargs.get("job_id")
        return get_object_or_404(JobPost, id=job_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        context["job"] = self.get_job()
        return context

    def perform_create(self, serializer):
        job = self.get_job()
        application = apply_to_job_service(
            user=self.request.user,
            job=job,
        )

        serializer.instance = application


class RespondToApplicationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]

    def get_object(self):
        return get_object_or_404(
            Application,
            id=self.kwargs["application_id"]
        )

    def update(self, request, *args, **kwargs):
        application = self.get_object()

        input_serializer = ApplicationStatusUpdateSerializer(
            data=request.data
        )
        input_serializer.is_valid(raise_exception=True)

        try:
            response = respond_to_application_service(
                application=application,
                responder=request.user,
                status=input_serializer.validated_data["status"],
                message=input_serializer.validated_data.get("message"),
            )
        except ForbiddenApplicationStatusUpdate:
            return Response(
                {"error": "You can't access to handle this application"},
                status=status.HTTP_403_FORBIDDEN
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            ApplicationResponseSerializer(response).data,
            status=status.HTTP_200_OK
        )
class WithdrawApplicationView(generics.DestroyAPIView):
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "application_id"

    def perform_destroy(self, instance):
        withdraw_application_service(user=self.request.user, instance=instance)

class UserApplicationsListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)

class JobApplicationsListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsJobOwner]

    def get_queryset(self):
        job_id = self.kwargs["job_id"]
        return Application.objects.filter(job_id=job_id)