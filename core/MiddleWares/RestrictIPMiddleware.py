from django.http import HttpResponseForbidden
from django.core.cache import cache
from decouple import config
from datetime import datetime

# Retrieve allowed IPs for Swagger
allowed_ips = config("SWAGGER_ALLOWED_IPS", default="")
ips_list = [ip.strip() for ip in allowed_ips.split(",") if ip.strip()]

class RestrictIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.key_ipv4 = "ipv4_cidrs"
        self.key_ipv6 = "ipv6_cidrs"
        
        # Initialize Cloudflare IPs for IPv4 and IPv6
        self.cloudflare_ipv4 = self.get_cloudflare_ips('V4', self.key_ipv4)
        self.cloudflare_ipv6 = self.get_cloudflare_ips('V6', self.key_ipv6)

    def get_cloudflare_ips(self, ip_type, cache_key):
        # Try to get IPs from cache
        ips = cache.get(cache_key)
        
        if ips is None:
            # Retrieve IPs from environment variables
            if ip_type == "V4":
                ips = [cidr.strip() for cidr in config("V4_CIDRS", default="").split(",") if cidr.strip()]
            else:
                ips = [cidr.strip() for cidr in config("V6_CIDRS", default="").split(",") if cidr.strip()]

            # Clean up and cache the IPs
            ips = [ip.strip() for ip in ips if ip.strip()]
            cache.set(cache_key, ips)
        
        return ips

    def __call__(self, request):
        # Get the client IP address
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        
        # Check for /service/health endpoint (allowed only for Cloudflare IPs)
        if request.path == "/service/health":
            time = datetime.now()
            print(f"{time} requester ip: {ip}")
            if not (ip in self.cloudflare_ipv4 or ip in self.cloudflare_ipv6 or ip in ips_list):
                return HttpResponseForbidden("Access Denied")

        # Check for /swagger/ endpoint (allowed only for specific IPs)
        if request.path == "/swagger/":
            time = datetime.now()
            print(f"{time} requester ip: {ip}")
            if ip not in ips_list:
                return HttpResponseForbidden("Access Denied")
            
        if request.path == "/service/logs":
            time = datetime.now()
            print(f"{time} requester ip: {ip}")
            if ip not in ips_list:
                return HttpResponseForbidden("Access Denied")
            
        if request.path == "/service/trends":
            time = datetime.now()
            print(f"{time} requester ip: {ip}")
            if ip not in ips_list:
                return HttpResponseForbidden("Access Denied")
        
        # Proceed to the next middleware/view
        return self.get_response(request)
