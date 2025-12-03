from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_user, name="register_user"),
    path("login/", views.LoginAPIView.as_view(), name="login")
]