from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

# from jobs.models import JobPost
# from .models import Application
from .serializers import LoginUserSerializer


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