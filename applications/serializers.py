from rest_framework.serializers import ModelSerializer
from .models import Application


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["status", "applicant", "job", "created_at", "updated_at"]