from rest_framework import serializers
from .models import Company


class CompanyBaseSerializer(serializers.ModelSerializer):
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

class PublicCompanySerializer(CompanyBaseSerializer):
    class Meta(CompanyBaseSerializer.Meta):
        pass
        
class OwnerCompanySerializer(CompanyBaseSerializer):
    class Meta(CompanyBaseSerializer.Meta):
        fields = CompanyBaseSerializer.Meta.fields + ["created_at"]