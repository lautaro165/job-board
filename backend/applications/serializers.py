from rest_framework import serializers

from .models import Application, ApplicationResponse, ApplicationStatus
from .services import apply_to_job_service

class _ApplicationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
        
class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["cover_letter", "resume"]

    def create(self, validated_data):
        user = self.context["request"].user
        job = self.context["job"]

        return apply_to_job_service(
            user=user,
            job=job,
            **validated_data
        )

class ApplicationListSerializer(_ApplicationBaseSerializer):
    job_id = serializers.IntegerField(source="job.id", read_only=True)
    
    class Meta(_ApplicationBaseSerializer.Meta):
        fields = _ApplicationBaseSerializer.Meta.fields + [
            "job_id",
        ]
        
class ApplicationDetailSerializer(_ApplicationBaseSerializer):
    class Meta(_ApplicationBaseSerializer.Meta):
        fields = _ApplicationBaseSerializer.Meta.fields + [
            "applicant",
            "job",
            "cover_letter",
            "resume",
        ]
        
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