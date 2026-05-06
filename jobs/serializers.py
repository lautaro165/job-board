from rest_framework.serializers import ModelSerializer
from .models import JobPost

class JobPostBaseSerializer(ModelSerializer):
    class Meta:
        model = JobPost
        fields = "__all__"
        
class JobPostListSerializer(JobPostBaseSerializer):
    class Meta(JobPostBaseSerializer.Meta):
        pass