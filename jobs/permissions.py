from rest_framework.permissions import BasePermission

from .models import JobPost

class IsJobOwner(BasePermission):
    def has_permission(self, request, view):
        job_id = view.kwargs.get("job_id")
        try:
            job = JobPost.objects.get(id=job_id)
        except JobPost.DoesNotExist:
            return False

        return job.owner == request.user