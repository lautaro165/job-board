import pytest

from rest_framework.test import APIClient

from django.urls import reverse

from applications.models import Application

@pytest.mark.django_db
def test_apply_to_job_authenticated(user_2, job):
    client = APIClient()

    client.force_authenticate(user=user_2)
    url = reverse("apply_to_job", kwargs={"job_id": job.id})

    response = client.post(url, {"cover_letter": "I am a good fit!"}, format="json")
    assert response.status_code == 201
    assert Application.objects.filter(applicant=user_2, job=job).exists()


@pytest.mark.django_db
def test_apply_to_job_unauthenticated(user_2, job):
    client = APIClient()
    
    url = reverse("apply_to_job", kwargs={"job_id": job.id})

    response = client.post(url, {"cover_letter": "Trying unauthenticated"}, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_apply_twice_to_same_job(user_2, job):
    client = APIClient()
    
    client.force_authenticate(user=user_2)
    url = reverse("apply_to_job", kwargs={"job_id": job.id})
    
    
    response1 = client.post(url, {"cover_letter": "First apply"}, format="json")
    assert response1.status_code == 201
    
    response2 = client.post(url, {"cover_letter": "Second apply"}, format="json")
    assert response2.status_code == 400


@pytest.mark.django_db
def test_apply_to_nonexistent_job(user_2):
    client = APIClient()
    
    client.force_authenticate(user=user_2)
    url = reverse("apply_to_job", kwargs={"job_id": 432})
    
    response = client.post(url, {"cover_letter": "Invalid job"}, format="json")
    assert response.status_code == 404

@pytest.mark.django_db
def test_respond_to_application(user, application):
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("responde_to_application", kwargs={"application_id": application.id})

    data = {
        "status":"rejected"
    }

    response = client.patch(url, data=data, format="json")

    application.refresh_from_db()

    assert response.status_code == 200
    assert application.status == "rejected"