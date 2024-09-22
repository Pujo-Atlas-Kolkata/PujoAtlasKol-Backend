from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F
from .models import Pujo
from .serializers import PujoSerializer, TrendingPujoSerializer
from core.ResponseStatus import ResponseStatus
import logging
from django.utils import timezone
from user.permission import IsSuperOrAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework import permissions

logger = logging.getLogger("pujo")

class PujoViewSet(viewsets.ModelViewSet):
    queryset = Pujo.objects.all()
    serializer_class = PujoSerializer
    lookup_field = 'id'
    permission_classes=[IsSuperOrAdminUser]
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'trending']:
            # Allow anyone to see list,trending and retreive
            return [permissions.AllowAny()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            search_params = request.query_params

            # Check if query parameters are provided
            if not search_params:
                # If no parameters are provided, return all records
                serializer = self.get_serializer(queryset, many=True)
                response_data = {
                    'result': serializer.data,
                    'status': ResponseStatus.SUCCESS.value
                }
                return Response(response_data, status=status.HTTP_200_OK)

            # Initialize a flag to track if any valid parameters were found
            valid_query_found = False

            # Check for valid query parameters
            if 'name' in search_params:
                queryset = queryset.filter(name__icontains=search_params.get('name').strip())
                valid_query_found = True
                # Increment searchScore only for name searches
                queryset.update(searchScore=F('searchScore') + 1)
            elif 'address' in search_params:
                queryset = queryset.filter(address__icontains=search_params.get('address').strip())
                valid_query_found = True
            elif 'city' in search_params:
                queryset = queryset.filter(city__icontains=search_params.get('city').strip())
                valid_query_found = True
            elif 'zone' in search_params:
                queryset = queryset.filter(zone__icontains=search_params.get('zone').strip())
                valid_query_found = True

            # If no valid query parameters were found, return an empty list
            if not valid_query_found:
                response_data = {
                    'result': {"message":"Not a valid query param","allowed_query_params":['name','address','city','zone']},
                    'status': ResponseStatus.SUCCESS.value
                }
                return Response(response_data, status=status.HTTP_200_OK)

            # Serialize the filtered queryset
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
    
    @action(detail=False, methods=['get'], url_path='trending')
    def trending(self, request, *args, **kwargs):
        try:
            trending_pujos = Pujo.objects.all().order_by('-searchScore')[:10]

            serializer = TrendingPujoSerializer(trending_pujos, many=True)
            
            response_data = {
                'result': serializer.data,
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error fetching trending Pujos: {str(e)}")
            response_data = {
                'error': str(e),
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, uuid=None, *args, **kwargs):
        try:
            pujo = self.get_queryset().filter(id=uuid).first()
            if pujo is None:
                response_data = {
                'result': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
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
        user = request.user
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'result': {'id': serializer.data["id"]},
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'error': serializer.errors,
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, uuid=None, *args, **kwargs):
        try:
            user = request.user
            self.check_object_permissions(request, user)
            pujo = self.get_queryset().filter(id=uuid).first()
            if pujo is None:
                response_data = {
                'result': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(pujo, data=request.data)
            if serializer.is_valid():
                serializer.save(updated_at=timezone.now())
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

    def destroy(self, request, uuid=None, *args, **kwargs):
        try:
            user = request.user
            self.check_object_permissions(request, user)
            pujo = self.get_queryset().filter(id=uuid).first()
            if pujo is None:
                response_data = {
                'result': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
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
