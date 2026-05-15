import pytest
import factory
from factory.django import DjangoModelFactory

from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser
from companies.models import Company
from jobs.models import JobPost
from jobs.choices import JobPostStatus, EmploymentTypes
from applications.models import Application


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save = True
    
    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.Sequence(lambda n: f'user_{n}@test.com')
    password = 'TestPass123!'
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = 'dev'
    is_active = True
    
    @factory.post_generation
    def set_password(obj, create, extracted):
        if not create:
            return
        obj.set_password(obj.password)
        obj.save()

class JobPostFactory(DjangoModelFactory):
    class Meta:
        model = JobPost
        skip_postgeneration_save = True
    
    title = factory.Sequence(lambda n: f'Job Title {n}')
    description = factory.Faker('paragraph')
    location = factory.Faker('city')
    status = JobPostStatus.ACTIVE
    employment_type = EmploymentTypes.FULL_TIME
    salary = factory.Faker('random_number', digits=5)

@pytest.fixture
def valid_job_post_data(company):
    return {
        'title': 'Software Engineer',
        'description': 'We are hiring',
        'company': company.id,
        'location': 'New York',
        'status': JobPostStatus.ACTIVE,
        'employment_type': EmploymentTypes.FULL_TIME,
        'salary': 120000,
    }

@pytest.fixture
def user():
    return CustomUser.objects.create_user(username="random_user",email="random_user@gmail.com",password="123456", role="dev")

@pytest.fixture
def company(user):
    return Company.objects.create(owner=user, name="random_company")

@pytest.fixture
def job(user,company):
    return JobPost.objects.create(posted_by=user,title="random_job",description="", company=company)

@pytest.fixture
def user_2():
    return CustomUser.objects.create_user(username="random_user_2",email="random_user_2@gmail.com",password="123456", role="dev")


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

@pytest.fixture
def user_factory():
    return CustomUserFactory

@pytest.fixture
def login_serializer_valid_data():
    return {
        'username': 'testuser',
        'password': 'TestPass123!'
    }

@pytest.fixture
def login_serializer_invalid_data():
    return {
        'username': 'nonexistent',
        'password': 'WrongPassword'
    }