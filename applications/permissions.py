from rest_framework.permissions import BasePermission
from jobs.models import JobPost


class IsJobOwner(BasePermission):
    message = "You are not the owner of this job posting."

    def has_object_permission(self, request, view, obj):
        return obj.job.posted_by == request.user
    
    def has_permission(self, request, view):
        job_id = view.kwargs.get("job_id")

        if not job_id:
            return True

        return JobPost.objects.filter(
            id=job_id,
            posted_by=request.user
        ).exists()

class IsApplicationOwnerOrJobOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.applicant == request.user or obj.job.posted_by == request.user
