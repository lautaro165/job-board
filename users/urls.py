from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register_user"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout/"),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path("me/", views.UserProfileView.as_view(), name="me")
]