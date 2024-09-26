from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F
from .models import Pujo
from .serializers import PujoSerializer, TrendingPujoSerializer, SearchedPujoSerializer
from core.ResponseStatus import ResponseStatus
import logging
from user.permission import IsSuperOrAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework import permissions
import re


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
            allowed_query_params = ['name', 'address', 'city', 'zone']
            search_params_filtered = {key: value for key, value in search_params.items() if key in allowed_query_params}

            # Ensure only one valid search parameter is provided
            if len(search_params_filtered) != 1:
                response_data = {
                    'result': {"message": "Only one search query param allowed at a time", 
                            "allowed_query_params": allowed_query_params},
                    'status': ResponseStatus.SUCCESS.value
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Check for valid query parameters
            if 'name' in search_params:
                search_value = search_params.get('name').strip()    
                # Generate the regex patterns based on the address
                regex_combinations = generate_regex_combinations(search_value)
                # Initialize an empty QuerySet for combined results
                results = Pujo.objects.none()  # An empty QuerySet of the Pujo model
                # Loop through each regex pattern and filter the queryset
                for regex in regex_combinations:
                    # Perform the regex search with case-insensitive matching
                    queryset = Pujo.objects.filter(name__iregex=regex) 
                    # Combine results from all regex matches (union of all results)
                    results = results | queryset
                valid_query_found = True
            elif 'address' in search_params:
                search_value = search_params.get('address').strip()    
                regex_combinations = generate_regex_combinations(search_value)
                results = Pujo.objects.none()
                for regex in regex_combinations:
                    queryset = Pujo.objects.filter(address__iregex=regex) 
                    results = results | queryset
                valid_query_found = True
            elif 'city' in search_params:
                search_value = search_params.get('city').strip()    
                regex_combinations = generate_regex_combinations(search_value)
                results = Pujo.objects.none()
                for regex in regex_combinations:
                    queryset = Pujo.objects.filter(city__iregex=regex) 
                    results = results | queryset
                valid_query_found = True
            elif 'zone' in search_params:
                search_value = search_params.get('zone').strip()    
                regex_combinations = generate_regex_combinations(search_value)
                results = Pujo.objects.none()
                for regex in regex_combinations:
                    queryset = Pujo.objects.filter(zone__iregex=regex) 
                    results = results | queryset
                valid_query_found = True

            # If no valid query parameters were found, return an empty list
            if not valid_query_found:
                response_data = {
                    'result': {"message":"Not a valid query param","allowed_query_params":allowed_query_params},
                    'status': ResponseStatus.SUCCESS.value
                }
                return Response(response_data, status=status.HTTP_200_OK)

            filtered_results = results.distinct('id')
            # Serialize the filtered queryset
            serializer = self.get_serializer(filtered_results, many=True)
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
                    'result': 'Given Pujo does not exist',
                    'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            # Increment the searchScore by 1
            pujo.searchScore += 1
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
                'result': str(e),
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def retrieve(self, request, uuid=None, *args, **kwargs):
        try:
            user = request.user
            self.check_permissions(request, user)
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
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
            pujo.delete()
            response_data = {
                'result': "Delete successful",
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Pujo.DoesNotExist:
            response_data = {
                'error': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
