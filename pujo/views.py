from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Pujo
from .serializers import PujoSerializer
from core.ResponseStatus import ResponseStatus
import logging

logger = logging.getLogger("pujo")

class PujoViewSet(viewsets.ModelViewSet):
    queryset = Pujo.objects.all()
    serializer_class = PujoSerializer
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            # Check for 'q' parameter in the query string
            search_query = request.query_params.get('q', '').strip()

            if search_query:
                queryset = queryset.filter(
                    Q(address__icontains=search_query) |
                    Q(name__icontains=search_query) |
                    Q(city__icontains=search_query) |
                    Q(zone__icontains=search_query)
                )

            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                'result': serializer.data,
                'status': ResponseStatus.SUCCESS.value
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching Pujo list: {str(e)}")
            response_data = {
                'error': str(e),
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            pujo = self.get_object()
            serializer = self.get_serializer(pujo)
            response_data = {
                'result': serializer.data,
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Pujo.DoesNotExist:
            response_data = {
                'result': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'result': {'id': serializer.data["uuid"]},
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'error': serializer.errors,
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            pujo = self.get_object()
            serializer = self.get_serializer(pujo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'result': serializer.data,
                    'status': ResponseStatus.SUCCESS.value
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'error': serializer.errors,
                    'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Pujo.DoesNotExist:
            response_data = {
                'result': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            pujo = self.get_object()
            pujo.delete()
            response_data = {
                'result': "Delete successful",
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Pujo.DoesNotExist:
            response_data = {
                'result': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
