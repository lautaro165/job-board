from rest_framework import serializers
from .models import Company


class PublicCompanySerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "description",
            "website",
            "logo",
            "followers_count",
        ]
        
class OwnerCompanySerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "description",
            "website",
            "logo",
            "created_at",
            "followers_count",
        ]