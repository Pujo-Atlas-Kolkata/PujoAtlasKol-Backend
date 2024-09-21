from rest_framework.permissions import BasePermission

class IsSuperOrAdminUser(BasePermission):
    """
    Custom permission to allow access only to super users or admin users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the appropriate user_type
        return request.user.is_authenticated and request.user.user_type in ['super user', 'admin user']

class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        print(obj)
        return request.user.is_authenticated and obj.owner == request.user