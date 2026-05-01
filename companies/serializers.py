from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)

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

class PublicCompanySerializer(CompanySerializer):
    pass
        
class OwnerCompanySerializer(CompanySerializer):
    class Meta(CompanySerializer.Meta):
        fields = CompanySerializer.Meta.fields + ["created_at"]