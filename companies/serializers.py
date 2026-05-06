from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class PublicCompanySerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = "__all__"

class OwnerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"