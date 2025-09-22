import pytest

from rest_framework.test import APIClient

from django.urls import reverse

from jobs.models import JobPost
from jobs.serializers import JobPostSerializer

# VIEWS TESTS

@pytest.mark.django_db
def test_job_post(user_tokens):
    client = APIClient()

    data = {
        "title":"IA Dev",
        "description":"Simple Description",
        "min_wage":100,
        "max_wage":200
    }

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_tokens["access"]}")
    response = client.post(reverse("post_job"),data=data)

    print("status_code".upper())
    print(response.status_code)

    assert response.status_code == 201