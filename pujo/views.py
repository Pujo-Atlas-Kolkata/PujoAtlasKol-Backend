from rest_framework import generics
from rest_framework.response import Response
from .models import Pujo
from .serializers import PujoSerializer
from django.db.models import Q
import logging

logger = logging.getLogger("pujo")

class PujoListView(generics.ListAPIView):
    serializer_class = PujoSerializer

    def get_queryset(self):
        queryset = Pujo.objects.all()

        # Check for 'q' parameter in the query string
        search_query = self.request.query_params.get('q', '').strip()
        
        if search_query:
            queryset = queryset.filter(
                Q(address__icontains=search_query)|
                Q(name__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(zone__icontains=search_query)
            )

        return queryset
