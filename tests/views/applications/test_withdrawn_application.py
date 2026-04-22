import pytest

from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_withdraw_application(user_2, testing_withdraw_application):
    
    client = APIClient()
    client.force_authenticate(user=user_2)
    url = reverse("withdraw_application", kwargs={"application_id": testing_withdraw_application.id})

    assert testing_withdraw_application.status == "pending"

    response = client.patch(url, format="json")
    testing_withdraw_application.refresh_from_db()

    assert "status" in response.data and response.data["status"] == "withdrawn"
    assert testing_withdraw_application.status == "withdrawn"
    assert response.status_code == 200