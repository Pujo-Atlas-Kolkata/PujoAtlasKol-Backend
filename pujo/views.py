from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F
from .models import Pujo
from .serializers import PujoSerializer, TrendingPujoSerializer, SearchedPujoSerializer, searchPujoSerializer
from core.ResponseStatus import ResponseStatus
import logging
from user.permission import IsSuperOrAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework import permissions
import re
from django.utils import timezone


logger = logging.getLogger("pujo")

def generate_regex_combinations(word):
    patterns = []
    length = len(word)

    # Basic pattern
    patterns.append(re.escape(word))

    # Inserting a wildcard (*) at the end
    patterns.append(word + r'.*')

    # Inserting a wildcard at the start
    patterns.append(r'.*' + word)

    patterns.append(word[0] +  r'[\w]{' + str(length - 2) + '}' + word[-1])

    patterns.append(r'.*' + word[0] +  r'[\w]{' + str(length - 2) + '}' + word[-1])

    patterns.append(word[0] +  r'[\w]{' + str(length - 2) + '}' + word[-1] + r'.*')
    
    # Patterns with wildcards and character classes
    for i in range(1, length-1):
        # Inserting [\w] at each position
        modified = word[:i] + r'[\w]' + word[i+1:]
        patterns.append(modified)

    return patterns


class PujoViewSet(viewsets.ModelViewSet):
    queryset = Pujo.objects.all()
    serializer_class = PujoSerializer
    lookup_field = 'id'
    permission_classes=[IsSuperOrAdminUser]
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ['list', 'trending', 'increase_search_score']:
            # Allow anyone to see list,trending and retreive
            return [permissions.AllowAny()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            # Check if query parameters are provided
            # If no parameters are provided, return all records
            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                    'result': serializer.data,
                    'message':'Pujo list successfully fetched',
                    'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'error': str(e),
                'status': ResponseStatus.FAIL.value
            }
            logger.error(f"Error: {response_data['error']}")
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], url_path='trending')
    def trending(self, request, *args, **kwargs):
        try:
            trending_pujos = Pujo.objects.all().order_by('-searchScore')[:10]

            serializer = TrendingPujoSerializer(trending_pujos, many=True)
            
            response_data = {
                'result': serializer.data,
                'message':'Trending pujo list fetched',
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            response_data = {
                'error': str(e),
                'status': ResponseStatus.FAIL.value
            }
            logger.error(f"Error: {response_data['error']}")
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def retrieve(self, request, uuid=None, *args, **kwargs):
        try:
            user = request.user
            self.check_permissions(request, user)
            pujo = self.get_queryset().filter(id=uuid).first()
            if pujo is None:
                response_data = {
                'error': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
                }
                user_id = request.user.id if request.user.is_authenticated else None
                logger.error(f"Error: {response_data['error']}", extra={'user_id': user_id})
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(pujo)
            response_data = {
                'result': serializer.data,
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Pujo.DoesNotExist:
            response_data = {
                'error': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
            }
            user_id = request.user.id if request.user.is_authenticated else None
            logger.error(f"Error: {response_data['error']}", extra={'user_id': user_id})
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        user = request.user
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'result': {'id': serializer.data["id"]},
                'message':'Pujo created',
                'status': ResponseStatus.SUCCESS.value
            }
            user_id = request.user.id if request.user.is_authenticated else None
            logger.info(f"Success: {response_data['message']}", extra={'user_id': user_id})
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'error': serializer.errors,
                'status': ResponseStatus.FAIL.value
            }
            user_id = request.user.id if request.user.is_authenticated else None
            logger.error(f"Error: {str(response_data['error'])}", extra={'user_id': user_id})
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, uuid=None, *args, **kwargs):
        try:
            user = request.user
            self.check_object_permissions(request, user)
            pujo = self.get_queryset().filter(id=uuid).first()
            if pujo is None:
                response_data = {
                'error': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
                }
                user_id = request.user.id if request.user.is_authenticated else None
                logger.error(f"Error: {response_data['error']}", extra={'user_id': user_id})
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(pujo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'result': serializer.data,
                    'message':f'Pujo updated',
                    'status': ResponseStatus.SUCCESS.value
                }
                user_id = request.user.id if request.user.is_authenticated else None
                logger.info(f"Success: {response_data['message']}", extra={'user_id': user_id})
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'error': serializer.errors,
                    'status': ResponseStatus.FAIL.value
                }
                user_id = request.user.id if request.user.is_authenticated else None
                logger.error(f"Error: {str(response_data['error'])}", extra={'user_id': user_id})
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Pujo.DoesNotExist:
            response_data = {
                'error': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
            }
            user_id = request.user.id if request.user.is_authenticated else None
            logger.error(f"Error: {response_data['error']}", extra={'user_id': user_id})
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, uuid=None, *args, **kwargs):
        try:
            user = request.user
            self.check_object_permissions(request, user)
            pujo = self.get_queryset().filter(id=uuid).first()
            if pujo is None:
                response_data = {
                'error': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
                }
                user_id = request.user.id if request.user.is_authenticated else None
                logger.error(f"Error: {response_data['error']}", extra={'user_id': user_id})
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
            pujo.delete()
            response_data = {
                'result': f"Delete successful for {str(uuid)}",
                'status': ResponseStatus.SUCCESS.value
            }
            user_id = request.user.id if request.user.is_authenticated else None
            logger.info(f"Success: {response_data['result']}", extra={'user_id': user_id})
            return Response(response_data, status=status.HTTP_200_OK)
        except Pujo.DoesNotExist:
            response_data = {
                'error': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
            }
            user_id = request.user.id if request.user.is_authenticated else None
            logger.error(f"Error: {response_data['error']}", extra={'user_id': user_id})
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class PujoTrendingIncreaseViewSet(viewsets.ModelViewSet):
    queryset = Pujo.objects.all()
    serializer_class = SearchedPujoSerializer
    lookup_field = 'id'
    
    @action(detail=False, methods=['post'], url_path='searched')
    def increase_search_score(self, request, *args, **kwargs):
        try:
            serializer = SearchedPujoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            uuid = serializer.validated_data['id']

            # Retrieve the Pujo instance
            pujo = self.get_queryset().filter(id=uuid).first()
            if pujo is None:
                response_data = {
                    'error': 'Given Pujo does not exist',
                    'status': ResponseStatus.FAIL.value
                }
                logger.error(f"Error: {response_data['error']}")
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            # Increment the searchScore by 1
            pujo.search_score += 1
            pujo.updated_at = timezone.now()
            pujo.save()

            updatedPujo = TrendingPujoSerializer(pujo)
            # Prepare the response with updated information
            response_data = {
                'result': updatedPujo.data,
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_data = {
                'error': str(e),
                'status': ResponseStatus.FAIL.value
            }
            logger.error(f"Error: {response_data['error']}")
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PujoSearchViewSet(viewsets.ModelViewSet):
    serializer_class = searchPujoSerializer

    def search_pujo(self, request, *args, **kwargs):
        try:
            # Validate the input data
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                search_term = serializer.validated_data['term'].strip()

                regex_combinations = generate_regex_combinations(search_term)

                # Initialize an empty QuerySet for combined results
                results = Pujo.objects.none()

                query_fields = ['name', 'address', 'city', 'zone']
                for regex in regex_combinations:
                    query_filter = Q()
                    for field in query_fields:
                        query_filter |= Q(**{f"{field}__iregex": regex})

                    results = results | Pujo.objects.filter(query_filter)

                # Remove duplicate entries based on the 'id'
                filtered_results = results.distinct("id")

                # Serialize the filtered queryset
                serializer = PujoSerializer(filtered_results, many=True)
                response_data = {
                    'result': serializer.data,
                    'status': ResponseStatus.SUCCESS.value
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                logger.error(f"Error: {str(serializer.errors)}")
                return Response({
                    'error': serializer.errors,
                    'status': ResponseStatus.FAIL.value
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response_data = {
                'error': str(e),
                'status': ResponseStatus.FAIL.value
            }
            logger.error(f"Error: {response_data['error']}")
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                