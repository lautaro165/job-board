from rest_framework.permissions import BasePermission


class IsJobOwner(BasePermission):
    message = "You are not the owner of this job posting."

    def has_object_permission(self, request, view, obj):
        return obj.job.owner == request.user
