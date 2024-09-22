from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.response import Response
from .ResponseStatus import ResponseStatus

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        response_data = {
            'error': str(exc),
            'status': ResponseStatus.FAIL.value
        }
        return Response(response_data, status=403)
    
    if isinstance(exc, PermissionDenied):
        response_data = {
            'error': str(exc),
            'status': ResponseStatus.FAIL.value
        }
        return Response(response_data, status=403)

    return response