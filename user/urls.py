from django.urls import path
from .views import UserViewSet, LoginView, LogoutView

# Define custom views for list and detail actions
# app_name = 'user'

user_create = UserViewSet.as_view({
    'post': 'create'  # Create action
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',    # Retrieve action
    'put': 'update',      # Update action
    'delete': 'destroy',   # Delete action
    'patch':'partial_update' # patch action
})

urlpatterns = [
    path('register', user_create, name='user_create'),  # URL for creating a new User
    path('<uuid:uuid>', user_detail, name='user_detail'),  # URL for detail, update, and delete
]
