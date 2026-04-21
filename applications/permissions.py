from rest_framework.permissions import BasePermission


class IsJobOwner(BasePermission):
    message = "You are not the owner of this job posting."

    def has_object_permission(self, request, view, obj):
        return obj.job.owner == request.user

class IsApplicationOwnerOrJobOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        # obj es una Application
        # Permitir si es el applicant o si es el job owner
        return obj.applicant == request.user or obj.job.owner == request.user
