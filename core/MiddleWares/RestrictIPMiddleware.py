from django.http import HttpResponseForbidden
import re

ALLOWED_IPS_Health_check = ["127.0.0.1"]  # Add more IPs if necessary

ALLOWED_IPS_swagger = ["127.0.0.1"]

ALLOWED_ORIGIN_REGEXES = [
    r"^https?://.*\.ourkolkata\.in$",
]

class RestrictIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        origin = request.META.get("HTTP_ORIGIN")
        print(origin)

        if origin:
            origin_allowed = any(re.match(pattern, origin) for pattern in ALLOWED_ORIGIN_REGEXES)
        
        if request.path == "/service/health":
            if ip not in ALLOWED_IPS_Health_check and not origin_allowed:
                return HttpResponseForbidden("Access Denied")
            
        if request.path == "/swagger/":
            if ip not in ALLOWED_IPS_swagger:
                return HttpResponseForbidden("Access Denied")
        
        response = self.get_response(request)
        return response
