import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request info
        logger.info(f"Request: {request.method} {request.get_full_path()}")

        # Call the next middleware or view
        response = self.get_response(request)

        # Log the response info
        logger.debug(f"Response: {response.status_code}")

        return response

    def process_exception(self, request, exception):
        logger.error(f"Exception occurred: {exception}")
