from applications.exceptions import ForbiddenApplicationStatusUpdate, TryingToApplyToOwnJob, ApplicationAlreadyExists, \
    InvalidUpdateStatus
from applications.models import Application, ApplicationResponse

from rest_framework.exceptions import ValidationError, PermissionDenied

VALID_RESPONSE_STATUSES = ["accepted", "rejected", "reviewed"]

def apply_to_job_service(user, job):

    if Application.objects.filter(applicant=user, job=job).exists():
        raise ApplicationAlreadyExists("You already applied this job")

    if user == job.posted_by:
        raise TryingToApplyToOwnJob("You cannot apply your own job")

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
    if application.job.posted_by != responder:
        raise ForbiddenApplicationStatusUpdate()

    if status not in VALID_RESPONSE_STATUSES:
        raise InvalidUpdateStatus()

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