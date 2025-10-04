from rest_framework.serializers import ModelSerializer
from .models import Application, ApplicationResponse


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["status", "applicant", "job", "created_at", "updated_at"]

    def create(self, validated_data):
        user = self.context["user"]
        job = self.context["job"]

        return Application.objects.create(applicant=user, job=job, **validated_data)
    
class ApplicationResponseSerializer(ModelSerializer):
    class Meta:
        model = ApplicationResponse
        fields = ["application", "responder", "message", "created_at"]