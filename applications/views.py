from django.shortcuts import get_object_or_404

from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework import status, generics

from jobs.models import JobPost
from .exceptions import ForbiddenApplicationStatusUpdate
from .models import Application
from .serializers import ApplicationSerializer, ApplicationResponseSerializer, ApplicationStatusUpdateSerializer
from .services import apply_to_job_service, respond_to_application_service, withdraw_application_service
from .permissions import IsJobOwner, IsApplicationOwnerOrJobOwner


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

class ApplicationDetailView(generics.RetrieveAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsApplicationOwnerOrJobOwner]

    queryset = Application.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "application_id"

class RespondToApplicationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsJobOwner]
    http_method_names = ["patch"]
    serializer_class = ApplicationStatusUpdateSerializer

    def get_object(self):
        return get_object_or_404(
            Application,
            id=self.kwargs["application_id"]
        )

    def update(self, request, *args, **kwargs):
        
        application = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = respond_to_application_service(
            application=application,
            responder=request.user,
            status=serializer.validated_data["status"],
            message=serializer.validated_data.get("message"),
        )
        
        return Response(
            ApplicationResponseSerializer(response).data,
            status=status.HTTP_200_OK
        )
    
class WithdrawApplicationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "application_id"
    lookup_field = "id"
    http_method_names = ["patch"]

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)

    def update(self, request, *args, **kwargs):
        application = self.get_object()

        updated_application = withdraw_application_service(
            user=request.user,
            application=application
        )

        return Response({
            "status": updated_application.status,
        })

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