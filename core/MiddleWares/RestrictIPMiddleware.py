from django.http import HttpResponseForbidden
import re

ALLOWED_IPS_Health_check = ["127.0.0.1"]  # Add more IPs if necessary

ALLOWED_IPS_swagger = ["127.0.0.1"]


class RestrictIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        print(x_forwarded_for)
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

        
        
        if request.path == "/service/health":
            if ip not in ALLOWED_IPS_Health_check:
                return HttpResponseForbidden("Access Denied")
            
        if request.path == "/swagger/":
            if ip not in ALLOWED_IPS_swagger:
                return HttpResponseForbidden("Access Denied")
        
        response = self.get_response(request)
        return response
