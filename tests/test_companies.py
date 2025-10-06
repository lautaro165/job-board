import pytest

from rest_framework.test import APIClient

from django.urls import reverse

from users.models import CustomUser


@pytest.mark.django_db
def test_valid_register_user():
    client = APIClient()

    data = {
        "username": "random_user",
        "email": "lautaro25@outlook.com.ar",
        "first_name": "user fistname",
        "last_name": "user lastname",
        "password": "valid_password"
    }
    
    response = client.post(reverse("register_user"), data=data)

    assert response.status_code == 201
    assert "tokens" in response.data
    assert "user" in response.data
    assert "message" in response.data