from rest_framework.throttling import SimpleRateThrottle


class OneMinuteThrottle(SimpleRateThrottle):
    scope = "one_minute"

    def get_cache_key(self, request, view):
        # Use the user's IP address as the cache key
        if request.user.is_authenticated:
            return f"{request.user.username}:{self.scope}"
        return request.META["REMOTE_ADDR"]
