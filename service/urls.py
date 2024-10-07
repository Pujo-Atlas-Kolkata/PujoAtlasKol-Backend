from django.urls import path
from .views import ServiceViewSet

# Define custom views for list and detail actions
health = ServiceViewSet.as_view({
    'get': 'health_check',    # List action
})


    # path('list', pujo_list, name='pujo-list'),  # URL for listing Pujos
    # path('add', pujo_create, name='pujo-create'),  # URL for creating a new Pujo
    # path('<uuid:uuid>', pujo_detail, name='pujo-detail'),  # URL for detail, update, and delete
    # path('list/trending', PujoViewSet.as_view({'get': 'trending'}), name='pujo-trending'),
    # path('searched', PujoTrendingIncreaseViewSet.as_view({'post':'increase_search_score'}), name='pujo-searched'),
    # path('search', PujoSearchViewSet.as_view({'post':'search_pujo'}), name="search-pujo")
urlpatterns = [
    path('health', health, name='health'),
    path('logs', ServiceViewSet.as_view({'get':'get_logs'}), name="logs")
]
