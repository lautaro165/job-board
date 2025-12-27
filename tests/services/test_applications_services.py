import pytest

from applications.services import apply_to_job_service
from rest_framework.exceptions import ValidationError
from applications.exceptions import TryingToApplyToOwnJob

@pytest.mark.django_db
def test_apply_to_job_service(user, job):
    with pytest.raises(ValidationError):
        apply_to_job_service(None, None)

    with pytest.raises(TryingToApplyToOwnJob):
        apply_to_job_service(user, job)