import pytest

from rest_framework.test import APIClient

from django.urls import reverse

from jobs.models import JobPost
from jobs.serializers import JobPostSerializer

# VIEWS TESTS

@pytest.mark.django_db
def test_post_job(user_tokens):
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

@pytest.mark.django_db
def test_edit_job_post(job, user_tokens):
    client = APIClient()
    
    updated_data = {
        "title": "Django Developer",
        "description": "Develop and maintain Django applications."
    }
    
    access_token = user_tokens["access"]
    
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    
    response = client.put(reverse("edit_job_post", kwargs={"job_id":job.id}),data=updated_data)
    
    job_instance = JobPost.objects.get(id=job.id)

    assert response.status_code == 200
    assert job_instance.title == updated_data["title"]
    assert job_instance.description == updated_data["description"]