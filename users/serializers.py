from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.exceptions import ValidationError

from .models import CustomUser

class CustomUserRegistrationSerializer(ModelSerializer):
    PASSWORD_MIN_LENGTH = 6

    password = CharField(write_only=True, min_length=PASSWORD_MIN_LENGTH)
    password2 = CharField(write_only=True, min_length=PASSWORD_MIN_LENGTH)

    class Meta:
        model=CustomUser
        fields=["id", "username", "email", "first_name", "last_name", "date_joined","role", "password", "password2"]

    def validate_email(self, value):
        
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError("This email is already in use")
        
        return value

    def validate_password2(self, value):
        
        if not value.strip():
            raise ValidationError("You must write your password twice.")
        
        return value

    def validate(self, data): 
        password = data.get("password")
        password2 = data.get("password2")

        if not password == password2:
            raise ValidationError("Passwords don't match")
        
        return data

    def create(self, validated_data):
        validated_data.pop("password")
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    
class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "first_name", "last_name","date_joined", "role"]
        read_only_fields = ["id", "email", "date_joined"]