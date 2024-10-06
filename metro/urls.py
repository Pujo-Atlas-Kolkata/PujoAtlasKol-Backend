from django.urls import path
from .views import TransportViewSet

transport_create = TransportViewSet.as_view({
    'post':'create'
})

transport_list = TransportViewSet.as_view({
    'get':'list'
})

transport_delete = TransportViewSet.as_view({
    'delete':'destroy'
})

urlpatterns = [
    path('list', transport_list, name='transport_list'),
    path('add', transport_create, name='create'),
    path('<uuid:uuid>', transport_delete, name='delete')
]
