from rest_framework.serializers import ModelSerializer
from .models import JobPost

class JobPostSerializer(ModelSerializer):
    class Meta:
        model = JobPost
        fields = "__all__"
        
class JobPostListSerializer(ModelSerializer):
    class Meta:
        model = JobPost
        fields = "__all__"