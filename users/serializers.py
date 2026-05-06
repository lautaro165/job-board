from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

from .models import CustomUser

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            
            if not user.is_active:
                raise serializers.ValidationError('User is disabled.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        refresh = RefreshToken.for_user(user)
        
        return {
            'user': user,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'access_expires': int(refresh.access_token.lifetime.total_seconds()),
            'refresh_expires': int(refresh.lifetime.total_seconds())
        }
    

# class CustomUserRegistrationSerializer(serializers.ModelSerializer):
#     PASSWORD_MIN_LENGTH = 6

#     password = serializers.CharField(write_only=True, min_length=PASSWORD_MIN_LENGTH)
#     password2 = serializers.CharField(write_only=True, min_length=PASSWORD_MIN_LENGTH)

#     class Meta:
#         model=CustomUser
#         fields=["id", "username", "email", "first_name", "last_name", "date_joined","role", "password", "password2"]

#     def validate_email(self, value):
        
#         if CustomUser.objects.filter(email=value).exists():
#             raise ValidationError("This email is already in use")
        
#         return value

#     def validate_password2(self, value):
        
#         if not value.strip():
#             raise ValidationError("You must write your password twice.")
        
#         return value

#     def validate(self, data): 
#         password = data.get("password")
#         password2 = data.get("password2")

#         if not password == password2:
#             raise ValidationError("Passwords don't match")
        
#         return data

#     def create(self, validated_data):
#         validated_data.pop("password")
#         validated_data.pop("password2")
#         user = CustomUser.objects.create_user(**validated_data)
#         return user
    
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "first_name", "last_name","date_joined", "role"]
        read_only_fields = ["id", "email", "date_joined"]