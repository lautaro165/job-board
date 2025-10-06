from rest_framework.serializers import ModelSerializer, CharField

from .models import CustomUser

class CustomUserRegistrationSerializer(ModelSerializer):
    password = CharField(write_only=True, min_length=6)
    
    class Meta:
        model=CustomUser
        fields=["id", "username", "email", "first_name", "last_name", "date_joined","role", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )
        return user
    
    
class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "first_name", "last_name","date_joined", "role"]
        read_only_fields = ["id", "email", "date_joined"]