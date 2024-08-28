from django.urls import path
from .views import PujoListView

urlpatterns = [
    path('list/', PujoListView.as_view(), name='pujo-list'),
]
