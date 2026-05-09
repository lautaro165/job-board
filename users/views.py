from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

# from jobs.models import JobPost
# from .models import Application
from .serializers import LoginUserSerializer, CustomUserRegistrationSerializer, LogoutSerializer


# Create your views here.

def get_user_tokens(user):
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    refresh_token_expires_time = int(refresh_token.lifetime.total_seconds())
    access_token_expires_time = int(access_token.lifetime.total_seconds())
    return refresh_token, access_token, refresh_token_expires_time, access_token_expires_time

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class RegisterUserView(generics.CreateAPIView):
    serializer_class = CustomUserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": "User registered successfully",
            "user": serializer.data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            {"message": "Successfully logged out."}, 
            status=status.HTTP_204_NO_CONTENT
        )