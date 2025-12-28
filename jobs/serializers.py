from rest_framework.serializers import ModelSerializer
from .models import JobPost

class JobPostSerializer(ModelSerializer):
    class Meta:
        model = JobPost
        fields = ["id", "title", "description", "owner", "company", "salary"]