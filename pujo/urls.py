from django.urls import path
from .views import PujoViewSet

# Define custom views for list and detail actions
pujo_list = PujoViewSet.as_view({
    'get': 'list',    # List action
})

pujo_create = PujoViewSet.as_view({
    'post': 'create'  # Create action
})

pujo_detail = PujoViewSet.as_view({
    'get': 'retrieve',    # Retrieve action
    'put': 'update',      # Update action
    'delete': 'destroy'   # Delete action
})

urlpatterns = [
    path('list', pujo_list, name='pujo-list'),  # URL for listing Pujos
    path('add', pujo_create, name='pujo-create'),  # URL for creating a new Pujo
    path('<uuid:uuid>', pujo_detail, name='pujo-detail'),  # URL for detail, update, and delete
    path('list/trending', PujoViewSet.as_view({'get': 'trending'}), name='pujo-trending')
]
