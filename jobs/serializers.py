from rest_framework.serializers import ModelSerializer, ChoiceField, CharField, Serializer

from .models import JobPost

class JobPostSerializer(ModelSerializer):
    class Meta:
        model = JobPost
        fields = ["id", "title", "description", "owner", "company", "min_wage", "max_wage"]
        
class ApplicationStatusUpdateSerializer(Serializer):
    status = ChoiceField(choices=["accepted", "rejected", "reviewed"])
    message = CharField()