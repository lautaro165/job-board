import pytest

from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser
from companies.models import Company
from jobs.models import JobPost
from applications.models import Application

@pytest.fixture
def user():
    return CustomUser.objects.create_user(username="random_user",email="random_user@gmail.com",password="123456", role="employee")

@pytest.fixture
def company(user):
    return Company.objects.create(created_by=user, name="random_company")

@pytest.fixture
def job(user,company):
    return JobPost.objects.create(owner=user,title="random_job",description="", company=company)

@pytest.fixture
def user_2():
    return CustomUser.objects.create_user(username="random_user_2",email="random_user_2@gmail.com",password="123456", role="employee")


@pytest.fixture
def application(user, job):
    return Application.objects.create(applicant=user, job=job)

@pytest.fixture
def testing_withdraw_application(user_2, job):
    return Application.objects.create(applicant=user_2, job=job)

@pytest.fixture
def user_tokens(user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    return {
        "refresh": str(refresh),
        "access": str(access),
        "refresh_token_expires_time": int(refresh.lifetime.total_seconds()),
        "access_token_expires_time": int(access.lifetime.total_seconds())
    }

@pytest.fixture
def user_2_tokens(user_2):
    refresh = RefreshToken.for_user(user_2)
    access = refresh.access_token
    return {
        "refresh": str(refresh),
        "access": str(access),
        "refresh_token_expires_time": int(refresh.lifetime.total_seconds()),
        "access_token_expires_time": int(access.lifetime.total_seconds())
    }

@pytest.fixture(scope="function")
def existing_test_user(django_db_blocker):
    with django_db_blocker.unblock():
        return CustomUser.objects.create_user(
            username="existing_user",
            email="random_user@outlook.com",
            password="somepassword"
        )