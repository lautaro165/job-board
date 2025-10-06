import pytest
import json

from rest_framework.test import APIClient

from django.urls import reverse

# from users.models import CustomUser

def load_invalid_cases():
    with open("tests/json_files/invalid_users_data.json", "r", encoding="utf-8") as file:
        invalid_cases = json.load(file)

    return invalid_cases

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

@pytest.mark.django_db
@pytest.mark.parametrize("case", load_invalid_cases())
def test_invalid_register_user(case):
    client = APIClient()
    
    response = client.post(reverse("register_user"), data=case)
    # expected_error = case.pop("expected_error_message")

    assert response.status_code == 400