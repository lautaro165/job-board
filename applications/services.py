from applications.models import Application
from rest_framework.exceptions import ValidationError

def apply_to_job(user, job):
    if Application.objects.filter(applicant=user).exists():
        raise ValidationError("You already applied this job")

    return Application.objects.create(
        applicant=user,
        job=job,
    )