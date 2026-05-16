from rest_framework import serializers

from .models import Application, ApplicationResponse, ApplicationStatus
from .services import apply_to_job_service

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "applicant", "job", "cover_letter", "resume", "status", "created_at", "updated_at"]
        read_only_fields = ["status", "applicant", "job", "created_at", "updated_at"]
        
    def create(self, validated_data):
        user = self.context["user"]
        job = self.context["job"]
        
        return apply_to_job_service(user=user, job=job)
    
class ApplicationResponseSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="application.status", read_only=True)
    
    class Meta:
        model = ApplicationResponse
        fields = ["application", "responder", "message", "created_at", "status"]

class ApplicationStatusUpdateSerializer(serializers.Serializer):
    
    ALLOWED_STATUSES = [
        ApplicationStatus.REVIEWED,
        ApplicationStatus.WITHDRAWN,
        ApplicationStatus.ACCEPTED,
        ApplicationStatus.REJECTED,
    ]
    
    status = serializers.ChoiceField(choices=ALLOWED_STATUSES)
    message = serializers.CharField(required=False, allow_blank=True)