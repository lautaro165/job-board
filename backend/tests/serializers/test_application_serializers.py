import pytest

from applications.serializers import ApplicationCreateSerializer, ApplicationStatusUpdateSerializer
from applications.choices import ApplicationStatus

class TestApplicationCreateSerializer:
    
    @pytest.mark.parametrize(
        'cover_letter_content', [
            'I am very interested in this position and believe my skills are a great match.',
            'Please find my application for the job opening. I look forward to hearing from you.',
            'I have attached my resume and cover letter for your review. Thank you for considering my application.',
            ''
        ]
    )
    @pytest.mark.django_db
    def test_serializer_valid_data(self, cover_letter_content, valid_pdf, authenticated_job_application_request):
        data = {
            'cover_letter': cover_letter_content,
            'resume': valid_pdf
        }
        
        serializer = ApplicationCreateSerializer(data=data, context=authenticated_job_application_request)
        
        assert serializer.is_valid(), serializer.errors
        
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "invalid_pdf_fixture",
        [
            "oversized_pdf",
            "invalid_extension_file",
            "fake_mime_pdf",
            "invalid_signature_pdf",
            "corrupted_integrity_pdf",
        ]
    )
    def test_invalid_application_serializer(
        self,
        request,
        authenticated_job_application_request,
        invalid_pdf_fixture
    ):
        invalid_pdf = request.getfixturevalue(invalid_pdf_fixture)

        data = {
            "cover_letter": "This is a valid cover letter.",
            "resume": invalid_pdf,
        }

        serializer = ApplicationCreateSerializer(
            data=data,
            context=authenticated_job_application_request
        )

        assert not serializer.is_valid()
        assert "resume" in serializer.errors
        
    @pytest.mark.django_db
    def test_serializer_missing_resume(self, authenticated_job_application_request):
        data = {
            'cover_letter': 'I am very interested in this position and believe my skills are a great match.',
        }
        
        serializer = ApplicationCreateSerializer(data=data, context=authenticated_job_application_request)
        
        assert not serializer.is_valid(), "Expected serializer to be invalid when resume is missing"
        assert 'resume' in serializer.errors, "Expected 'resume' field to have validation errors"

class TestApplicationListSerializer:
    pass

class TestApplicationDetailSerializer:
    pass

class TestApplicationResponseSerializer:
    pass

class TestApplicationStatusUpdateSerializer:
    
    @pytest.mark.parametrize(
        ['status', 'message'],
        [
            (ApplicationStatus.ACCEPTED, 'Application submitted successfully.'),
            (ApplicationStatus.ACCEPTED, 'Application approved.'),
            (ApplicationStatus.REJECTED, 'Application rejected.'),
            (ApplicationStatus.WITHDRAWN, ''),
            (ApplicationStatus.REVIEWED, ''),
            (ApplicationStatus.ACCEPTED, ''),
        ]
    )
    def test_serializer_valid_updates(self, status, message):
        data = {
            'status': status,
            'message': message
        }
        
        serializer = ApplicationStatusUpdateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        
    @pytest.mark.parametrize(
        ['status', 'message'],
        [
            (ApplicationStatus.PENDING, 'Application pending.'),
        ]
    )
    def test_serializer_invalid_updates(self, status, message):
        data = {
            'status': status,
            'message': message
        }

        serializer = ApplicationStatusUpdateSerializer(data=data)
        assert not serializer.is_valid(), "Expected serializer to be invalid"
        assert 'status' in serializer.errors, "Expected 'status' field to have validation errors"