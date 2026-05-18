from factory import SubFactory, LazyAttribute
from factory.django import DjangoModelFactory

from django.core.files.uploadedfile import SimpleUploadedFile

from applications.models import Application

from tests.factories.users import CustomUserFactory
from tests.factories.jobs import JobPostFactory


class ApplicationFactory(DjangoModelFactory):
    class Meta:
        model = Application

    job = SubFactory(JobPostFactory)
    applicant = SubFactory(CustomUserFactory)
    resume = LazyAttribute(
        lambda _: SimpleUploadedFile(
            "resume.pdf",
            b"Fake PDF content",
            content_type="application/pdf"
        )
    )