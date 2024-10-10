from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.ResponseStatus import ResponseStatus
from pujo.models import LastScoreModel
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
import pandas as pd
import django
import platform
import os
from datetime import datetime, timedelta
from django.db import connection
from decouple import config
import http.client
import json
import csv
from django.http import HttpResponse
from io import StringIO
from datetime import datetime
from collections import defaultdict
from .helper import get_memory_info, kb_to_mb, get_disk_usage, get_cpu_usage

APP_START_TIME = datetime.now()


class ServiceViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.action in ["health_check"]:
            # Allow anyone to see list,trending and retreive
            return [permissions.AllowAny()]
        return super().get_permissions()

    def health_check(request, *args, **kwargs):
        data = {}
        status_code = 200

        memory_info = get_memory_info()

        # Extract specific memory details
        total_memory = kb_to_mb(memory_info.get("MemTotal"))
        free_memory = kb_to_mb(memory_info.get("MemFree"))
        available_memory = kb_to_mb(memory_info.get("MemAvailable"))

        used_memory = total_memory - available_memory

        used_memory_percentage = (used_memory / total_memory) * 100

        data["free_memory"] = f"{free_memory:.2f} MB"
        data["total_memory"] = f"{total_memory:.2f} MB"
        data["memory_usage"] = f"{used_memory_percentage:.2f} %"

        disk_usage = get_disk_usage("/")

        total_disk_space_gb = disk_usage["total_space_mb"] / 1024
        disk_usage_percentage = (
            disk_usage["used_space_mb"] / disk_usage["total_space_mb"]
        ) / 100

        data["total_space_mb"] = f"{disk_usage['total_space_mb']:.2f} MB"
        data["used_space_mb"] = f"{disk_usage['used_space_mb']:.2f} MB"
        data["free_space_mb"] = f"{disk_usage['free_space_mb']:.2f} MB"
        data["disk_usage_percentage"] = (
            f"{disk_usage_percentage:.2f} % of {total_disk_space_gb:.2f}"
        )

        cpu_usage = get_cpu_usage()

        data["cpu_usuage"] = f"{cpu_usage:.2f}%"

        # Check app status
        data["status"] = "OK"

        # Uptime
        current_time = datetime.now()
        uptime = current_time - APP_START_TIME
        data["uptime"] = str(timedelta(seconds=uptime.total_seconds()))

        # Application version (can be set in an environment variable)
        data["app_version"] = "1.1.0"

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

        response_data = {"result": data, "status": ResponseStatus.SUCCESS.value}

        return Response(response_data, status=status_code)

    # def get_logs(request, *args, **kwargs):
    #     url = config('NODE_API_URL')
    #     endpoint = config('NODE_ENDPOINT')

    #     try:
    #         connection = http.client.HTTPConnection(url)
    #         connection.request("GET", endpoint)
    #         response = connection.getresponse()

    #         if response.status == 200:
    #             data = response.read().decode('utf-8')
    #             try:
    #                 parsed_data = json.loads(data)
    #             except json.JSONDecodeError as e:
    #                 print("Failed to decode JSON:", e)
    #             connection.close()

    #             # Debugging: Print the raw data and parsed data
    #             # print("Raw data from API:", data)  # Show raw data
    #             # print("Parsed data:", parsed_data)  # Show parsed data

    #             if not isinstance(parsed_data, dict):
    #                 return Response({'error': 'Unexpected data format', "status":ResponseStatus.FAIL.value}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #             # Check if the 'result' key exists
    #             if 'system_logs' not in parsed_data:
    #                 return Response({'error': 'No system_logs key in response', "status":ResponseStatus.FAIL.value}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #             # Extract the system_logs from the parsed data
    #             system_logs = parsed_data.get('system_logs')

    #             message = parsed_data.get('message')

    #             # This will be True if system_logs is an empty list
    #             if not system_logs:
    #                 return Response({'error': message, "status":ResponseStatus.FAIL.value}, status=status.HTTP_200_OK)

    #             # Prepare in-memory CSV file
    #             csv_file = StringIO()
    #             writer = csv.writer(csv_file)

    #             # Ensure system_logs is a list before proceeding
    #             if isinstance(system_logs, list) and system_logs:
    #                 # Write header (keys of the first dict)
    #                 writer.writerow(system_logs[0].keys())
    #                 # Write the rows (values)
    #                 for row in system_logs:
    #                     writer.writerow(row.values())

    #                 # Get the current date and time for the file name
    #                 now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    #                 file_name = f"logs_{now}.csv"

    #                 # Prepare HttpResponse with CSV content and dynamic file name
    #                 csv_response = HttpResponse(content_type='text/csv')
    #                 csv_response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    #                 csv_response.write(csv_file.getvalue())
    #                 csv_file.close()  # Close the StringIO

    #                 csv_response['X-Message'] = message

    #                 # Return the CSV file response
    #                 return csv_response

    #             else:
    #                 connection.close()
    #                 return Response({'error': 'No logs found or unexpected data format', "status":ResponseStatus.FAIL.value}, status=status.HTTP_400_BAD_REQUEST)

    #         else:
    #             connection.close()
    #             return Response({'error': 'Failed to fetch logs', "status":ResponseStatus.FAIL.value}, status=response.status)

    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def show_trends(requset, *args, **kwargs):
        data = LastScoreModel.objects.all()

        trends = defaultdict(lambda: {"values": [], "ts": []})

        for score in data:
            trends[score.pujo_id]["values"].append(score.value)
            trends[score.pujo_id]["ts"].append(score.last_updated_at)

        # Convert defaultdict to a list of dictionaries
        result = [
            {"pujo_id": pujo_id, "values": data["values"], "ts": data["ts"]}
            for pujo_id, data in trends.items()
        ]

        # Return the result (in your case, you'd return it as a response)
        return Response({"result": result, "status": ResponseStatus.SUCCESS.value})
