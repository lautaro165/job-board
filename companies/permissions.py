from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCompanyOwner(BasePermission):
    message = "Only the company owner can modify this company"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by == request.user