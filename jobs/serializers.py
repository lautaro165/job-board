from rest_framework.serializers import ModelSerializer
from .models import JobPost

class _JobPostBaseSerializer(ModelSerializer):
    class Meta:
        model = JobPost
        fields = "__all__"
        
class JobPostListSerializer(_JobPostBaseSerializer):
    class Meta(_JobPostBaseSerializer.Meta):
        pass