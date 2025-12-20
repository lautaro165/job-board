from applications.exceptions import ForbiddenApplicationStatusUpdate
from applications.models import Application, ApplicationResponse
from rest_framework.exceptions import ValidationError

def apply_to_job_service(user, job):
    if Application.objects.filter(applicant=user).exists():
        raise ValidationError("You already applied this job")

    return Application.objects.create(
        applicant=user,
        job=job,
    )

def respond_to_application_service(
    application,
    responder,
    status,
    message=None
):
    if application.job.owner != responder:
        raise ForbiddenApplicationStatusUpdate()

    application.status = status
    application.save()

    return ApplicationResponse.objects.create(
        application=application,
        responder=responder,
        message=message,
    )