from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# from jobs.models import JobPost
# from .models import Application
from django.contrib.auth import authenticate
from .serializers import CustomUserSerializer, CustomUserRegistrationSerializer

# Create your views here.

def get_user_tokens(user):
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    refresh_token_expires_time = int(refresh_token.lifetime.total_seconds())
    access_token_expires_time = int(access_token.lifetime.total_seconds())
    return refresh_token, access_token, refresh_token_expires_time, access_token_expires_time

@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    
    if not (username and password):
        return Response({"error":"You must provide a username and a password"},status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=username, password=password)
    
    if user is None:
        return Response({"error":"Invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)
    
    refresh_token, access_token, refresh_token_expires_time, access_token_expires_time = get_user_tokens(user)
        
    return Response({
        "refresh": str(refresh_token),
        "access": str(access_token),
        "refresh_token_expires_time": refresh_token_expires_time,
        "access_token_expires_time": access_token_expires_time
    }, status=status.HTTP_200_OK)

@api_view(["POST"])
def register_user(request):
    serializer = CustomUserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "User registered successfully",
            "user": CustomUserSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)