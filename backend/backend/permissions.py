from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """
    Custom permission to only allow superusers to access a view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
class IsStaff(BasePermission):
    """
    Custom permission to only allow superusers to access a view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
