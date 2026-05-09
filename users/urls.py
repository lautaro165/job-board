from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register_user"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]