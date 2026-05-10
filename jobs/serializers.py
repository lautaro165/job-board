from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import JobPost

class JobPostSerializer(ModelSerializer):
    class Meta:
        model = JobPost
        fields = "__all__"
        read_only_fields = ('posted_by','company')
    
    def validate_company(self, value):
        
        user = self.context['request'].user
        
        is_owner = value.posted_by == user
        is_admin = value.admins.filter(id=user.id).exists()

        if not (is_owner or is_admin):
            raise ValidationError(
                "You cannot post new jobs in this Company"
            )
        
        return value
        
class JobPostListSerializer(ModelSerializer):
    class Meta:
        model = JobPost
        fields = "__all__"