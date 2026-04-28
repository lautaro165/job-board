from rest_framework.serializers import ModelSerializer, Serializer, CharField, ChoiceField
from rest_framework.serializers import ValidationError

from .models import Application, ApplicationResponse, ApplicationStatus
from .services import apply_to_job_service

class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["status", "applicant", "job", "created_at", "updated_at"]
        
    def create(self, validated_data):
        user = self.context["user"]
        job = self.context["job"]
        
        return apply_to_job_service(user=user, job=job)
    
class ApplicationResponseSerializer(ModelSerializer):
    class Meta:
        model = ApplicationResponse
        fields = ["application", "responder", "message", "created_at"]

class ApplicationStatusUpdateSerializer(Serializer):
    status = ChoiceField(choices=ApplicationStatus.choices)
    message = CharField(required=False, allow_blank=True)