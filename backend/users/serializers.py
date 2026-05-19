from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from users.models import CustomUser

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
            'user': UserProfileInfoSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'access_expires': int(refresh.access_token.lifetime.total_seconds()),
            'refresh_expires': int(refresh.lifetime.total_seconds())
        }


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    password2 = serializers.CharField(write_only=True, min_length=8, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role', 'password', 'password2']
        
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError(f"{value} is already in use.")
        
        return value
    
    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")
        
        if password != password2:
            raise ValidationError("Provided password don't match")
        
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role"
        ]
        read_only_fields = ["email"]
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError({'refresh': 'Invalid or expired token'})
        
class UpdateUserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password2 = serializers.CharField(write_only=True, min_length=8)
    
    def validate_old_password(self, value):
        user = self.context["user"]
        
        if not user.check_password(value):
            raise ValidationError("Provided password is not correct.")
        
        return value
    
    def validate(self, data):
        new_password = data.get("new_password")
        new_password2 = data.get("new_password2")
        
        if new_password != new_password2:
            raise ValidationError("Provided new passwords don't match.")
        
        validate_password(new_password, user=self.context["user"])
        
        return data
    
    def save(self):
        
        user = self.context["user"]
        
        user.set_password(self.validated_data["new_password"])
        user.save()
        
        return user