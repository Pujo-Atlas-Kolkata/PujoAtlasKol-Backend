from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Pujo
from .serializers import PujoSerializer
from django.db.models import Q
from core.ResponseStatus import ResponseStatus
import logging

logger = logging.getLogger("pujo")

@api_view(['GET'])
def getPujoList(request):
    if request.method == 'GET':
        try:
            queryset = Pujo.objects.all()

            # Check for 'q' parameter in the query string
            search_query = request.query_params.get('q', '').strip()

            if search_query:
                    queryset = queryset.filter(
                        Q(address__icontains=search_query)|
                        Q(name__icontains=search_query) |
                        Q(city__icontains=search_query) |
                        Q(zone__icontains=search_query)
                    )

            serializer = PujoSerializer(queryset, many=True)

            response_data = {
                        'result': serializer.data,
                        'status': ResponseStatus.SUCCESS.value
                    }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            # Return an error response
            response_data = {
                'error': str(e),
                'status': ResponseStatus.FAIL.value
            }

            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'status': 'error', 'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

