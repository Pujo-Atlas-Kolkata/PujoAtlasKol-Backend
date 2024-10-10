from rest_framework.throttling import SimpleRateThrottle


class OneMinuteThrottle(SimpleRateThrottle):
    scope = "one_minute"

    def get_cache_key(self, request, view):
        # Use the user's IP address as the cache key
        return request.META.get("REMOTE_ADDR")
