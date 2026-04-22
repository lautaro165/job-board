import pytest

from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_respond_to_application(user, application):
    
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("respond_to_application", kwargs={"application_id": application.id})

    data = {"status": "rejected"}
    response = client.patch(url, data=data, format="json")

    application.refresh_from_db()

    assert response.status_code == 200
    assert application.status == "rejected"