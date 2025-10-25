import pytest
import json

from rest_framework.test import APIClient

from django.urls import reverse

from users.models import CustomUser


def load_registration_cases():
    with open("tests/json_files/users_data_cases.json", "r", encoding="utf-8") as file:
        cases = json.load(file)

    return cases

@pytest.mark.django_db
@pytest.mark.parametrize("case", load_registration_cases())
def test_register_user(case, existing_test_user):
    client = APIClient()
    
    expected_status_code = case.pop("expected_status_code")
    
    response = client.post(reverse("register_user"), data=case)

    assert response.status_code == expected_status_code, f"The gotten status code {response.status_code} does not match with the expected one: {expected_status_code}"

    if response.status_code == 201:

        assert "message" in response.data
        assert "user" in response.data
        assert "tokens" in response.data

        user = response.data["user"]
        
        assert user["username"] == case["username"], "username was not registered successfully"
        assert user["email"] == case["email"], "email was not registered successfully"
        assert user["first_name"] == case["first_name"], "first name was not registered successfully"
        assert user["last_name"] == case["last_name"], "last name was not registered successfully"

        assert CustomUser.objects.filter(username=user["username"], email=user["email"]).exists(), f"User '{user["username"]}' should have been created but was not."
    else:
        assert not CustomUser.objects.filter(username=case["username"], email=case["email"]).exists(), f"User '{case["username"]}' should NOT exist but was found in the DB."