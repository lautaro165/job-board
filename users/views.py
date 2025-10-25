from rest_framework.decorators import api_view
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# from jobs.models import JobPost
# from .models import Application
from .serializers import CustomUserSerializer, CustomUserRegistrationSerializer

# Create your views here.

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