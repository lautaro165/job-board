from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import authenticate, get_user_model

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
            'user': user,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'access_expires': int(refresh.access_token.lifetime.total_seconds()),
            'refresh_expires': int(refresh.lifetime.total_seconds())
        }


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
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