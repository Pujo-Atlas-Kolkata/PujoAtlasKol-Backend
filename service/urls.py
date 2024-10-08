from django.urls import path
from .views import ServiceViewSet

# Define custom views for list and detail actions
health = ServiceViewSet.as_view({
    'get': 'health_check',
})

logs = ServiceViewSet.as_view({'get':'get_logs'})

trends = ServiceViewSet.as_view({'get':'show_trends'})


urlpatterns = [
    path('health', health, name='health'),
]
    # path('trends', trends, name="trends")
    # path('logs', logs, name="logs"),
