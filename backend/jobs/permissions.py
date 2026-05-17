from rest_framework.permissions import BasePermission

from .models import JobPost

class IsJobOwner(BasePermission):
    message = "You are not allowed to perform this action"

    def has_object_permission(self, request, view, obj):
    
        return obj.posted_by == request.user or obj.company.owner == request.user