import pytest
from unittest.mock import patch, MagicMock
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import TokenError

from jobs.serializers import JobPostSerializer, JobPostListSerializer


class TestJobPostSerializer:
    
    @pytest.mark.parametrize(
        'missing_field',
        [
            'title',
            'description',
            'location',
        ]
    )
    @pytest.mark.django_db
    def test_serializer_missing_required_fields(self, missing_field, valid_job_post_data):
        
        data = valid_job_post_data.copy()
        
        data.pop(missing_field)
        
        serializer = JobPostSerializer(data=data)
        assert not serializer.is_valid()
        
    @pytest.mark.parametrize(
        'missing_field',
        [
            "company",
            "salary",
            "employment_type",
            "status",
        ]
    )
    @pytest.mark.django_db
    def test_serializer_missing_not_required_fields(self, missing_field, valid_job_post_data):
        
        data = valid_job_post_data.copy()
        
        data.pop(missing_field)
        
        serializer = JobPostSerializer(data=data)
        assert serializer.is_valid(), serializer.errors