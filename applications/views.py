from django.shortcuts import get_object_or_404

from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework import status, generics

from jobs.models import JobPost
from jobs.permissions import IsJobOwner
from .models import Application
from .serializers import ApplicationSerializer, ApplicationResponseSerializer, ApplicationStatusUpdateSerializer
from .services import apply_to_job


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
        application = apply_to_job(
            user=self.request.user,
            job=job,
        )

        serializer.instance = application


class RespondToApplicationView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["patch"]

    def get_object(self):
        application_id = self.kwargs["application_id"]
        return get_object_or_404(Application, id=application_id)

    def update(self, request, *args, **kwargs):
        application = self.get_object()

        if request.user != application.job.owner:
            return Response(
                {"error": "You can't access to handle this application"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ApplicationStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        status_value = serializer.validated_data.get("status", None)
        message = serializer.validated_data.get("message", None)

        application.status = status_value
        application.save()

        response_serializer = ApplicationResponseSerializer(data={
            "application": application.id,
            "responder": request.user.id,
            "message": message,
        })
        response_serializer.is_valid(raise_exception=True)
        response = response_serializer.save()

        return Response(
            ApplicationResponseSerializer(response).data,
            status=status.HTTP_200_OK
        )


class WithdrawApplicationView(generics.DestroyAPIView):
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "application_id"

    def perform_destroy(self, instance):
        if instance.applicant != self.request.user:
            raise PermissionDenied("You cannot withdraw an application that is not yours")
        instance.delete()

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