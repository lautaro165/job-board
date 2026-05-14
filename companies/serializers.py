from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "description", "website"]

class PublicCompanySerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = ["id", "name", "description", "website", "followers_count"]

class OwnerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "description", "website", "created_at", "updated_at"]