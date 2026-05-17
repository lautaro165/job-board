from rest_framework import status
from rest_framework.exceptions import APIException

class InvalidUpdateStatus(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid update status'

class ForbiddenApplicationStatusUpdate(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You are not authorized to update this application'

class ApplicationAlreadyExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Application already exists'

class TryingToApplyToOwnJob(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Trying to apply to own job'
    
class JobNotAvailable(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Job is not available for applications'