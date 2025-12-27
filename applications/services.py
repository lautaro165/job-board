from applications.exceptions import ForbiddenApplicationStatusUpdate
from applications.models import Application, ApplicationResponse

from rest_framework.exceptions import ValidationError, PermissionDenied

from debug import print_debug_message

VALID_RESPONSE_STATUSES = ["accepted", "rejected", "reviewed"]

def apply_to_job_service(user, job):
    if Application.objects.filter(applicant=user).exists():
        raise ValidationError("You already applied this job")

    if user == job.owner:
        raise ValidationError("You cannot apply your own job")

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

    if status not in VALID_RESPONSE_STATUSES:
        raise ValueError("Invalid status")

    application.status = status
    application.save()

    return ApplicationResponse.objects.create(
        application=application,
        responder=responder,
        message=message,
    )

def withdraw_application_service(user, application):
    if application.applicant != user:
        raise PermissionDenied("You cannot withdraw an application that is not yours")

    application.status = "withdrawn"
    application.save()

    return application