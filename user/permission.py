from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from .models import BlacklistedToken

class IsSuperOrAdminUser(BasePermission):
    """
    Custom permission to allow access only to super users or admin users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the appropriate user_type
        return request.user.is_authenticated and request.user.user_type in ['superadmin', 'admin']
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        tokenHeader = request.META.get('HTTP_AUTHORIZATION')
        if tokenHeader is None or not tokenHeader.startswith('Bearer '):
            raise AuthenticationFailed('Authorization header missing or malformed')

        token = tokenHeader.split()[1]  # Extract the token
        if token:
            try:
                if BlacklistedToken.objects.filter(token=token).exists():
                    raise PermissionDenied("This token has been blacklisted.")
                else:
                    access_token = AccessToken(token)  # Validate the token
                    user_id_from_token = access_token['user_id']
            except Exception:
                raise AuthenticationFailed('Token is invalid or expired')

        # Check if the user_id from the token matches the logged-in user
        if str(request.user.id) != str(user_id_from_token):
            raise AuthenticationFailed('User ID does not match the authenticated user')
        else:
            return True

class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Verify JWT token and check user ID
        try:
            tokenHeader = request.META.get('HTTP_AUTHORIZATION')
            if tokenHeader is None or not tokenHeader.startswith('Bearer '):
                raise AuthenticationFailed('Authorization header missing or malformed')

            token = tokenHeader.split()[1]  # Extract the token
            if token:
                if BlacklistedToken.objects.filter(token=token).exists():
                    raise PermissionDenied("This token has been blacklisted.")
                else:
                    access_token = AccessToken(token)
                    user_id_from_token = access_token['user_id']  # Extract user ID from token
                    
                    # Compare the user ID from the token with the requested object's user ID
                    return str(user_id_from_token) == str(obj.id)
            else:
                raise PermissionDenied('Token Not found')
        except (IndexError, KeyError, AuthenticationFailed):
            return False