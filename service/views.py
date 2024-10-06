from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.ResponseStatus import ResponseStatus
from user.permission import IsSuperOrAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
import pandas as pd
import django
import platform
import os
from datetime import datetime, timedelta
from django.db import connection

APP_START_TIME = datetime.now()

class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes=[IsSuperOrAdminUser]
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ['health_check']:
            # Allow anyone to see list,trending and retreive
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def health_check(request, *args, **kwargs):
        data = {}
        status_code = 200

        # Check app status
        data["status"] = "OK"

        # Uptime
        current_time = datetime.now()
        uptime = current_time - APP_START_TIME
        data["uptime"] = str(timedelta(seconds=uptime.total_seconds()))

        # Application version (can be set in an environment variable)
        data["app_version"] = os.getenv("APP_VERSION", "1.0.0")

        # Django version
        data["django_version"] = django.get_version()

        # Python version
        data["python_version"] = platform.python_version()

        # Database connection check
        try:
            connection.ensure_connection()
            data["database"] = "Connected"
        except Exception as e:
            data["database"] = f"Failed ({str(e)})"
            status_code = 500

        # Server time
        data["server_time"] = current_time.isoformat()

        response_data = {
            "result":data,
            "status":ResponseStatus.SUCCESS.value
        }

        return Response(response_data, status=status_code)

    


