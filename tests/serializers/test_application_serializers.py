import pytest

from applications.serializers import ApplicationStatusUpdateSerializer
from applications.choices import ApplicationStatus

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
        
class TestApplicationResponseSerializer:
    pass