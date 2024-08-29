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
    response_data = {
                'result': 'Method not allowed',
                'status': ResponseStatus.FAIL.value
            }
    return Response(response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
def getPujoDetail(request, pk):
    if request.method == 'GET':
        if pk is not None:
            try:
                pujo = Pujo.objects.get(uuid=pk)
                data = PujoSerializer(pujo).data
                response_data = {
                        'result': data,
                        'status':ResponseStatus.SUCCESS.value
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Pujo.DoesNotExist:
                response_data = {
                'result': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        else:
            response_data = {
                'result':'Not a valid id',
                'status':ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)    
    # default case
    response_data = {
                    'result': 'Method not allowed',
                    'status': ResponseStatus.FAIL.value
                    }           
    return Response(response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def addNewPujo(request):
    if request.method == 'POST':
        serializer = PujoSerializer(data=request.data)
        if serializer.is_valid():       
            serializer.save()
            response_data={
                'result':{'id':serializer.data["uuid"]},
                'status':ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'error': serializer.errors,
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    # default case
    response_data = {
                    'result': 'Method not allowed',
                    'status': ResponseStatus.FAIL.value
                    }           
    return Response(response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT'])
def updatePujoDetails(request,pk):
    if request.method == 'PUT':
        if pk is not None:
            try:
                pujo = Pujo.objects.get(uuid=pk)
                serializer = PujoSerializer(pujo, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response_data={
                        'result':serializer.data,
                        "status":ResponseStatus.SUCCESS.value
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
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
        else:
            response_data = {
                'result':'Not a valid id',
                'status':ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)    
    # default case
    response_data = {
                    'result': 'Method not allowed',
                    'status': ResponseStatus.FAIL.value
                    }           
    return Response(response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['DELETE'])
def DeletePujo(request,pk):
    if request.method == 'DELETE':
        if pk is not None:
            try:
                pujo = Pujo.objects.get(uuid=pk)
                pujo.delete()
                response_data = {
                        'result': "Delete successful",
                        'status':ResponseStatus.SUCCESS.value
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Pujo.DoesNotExist:
                response_data = {
                'result': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        else:
            response_data = {
                'result':'Not a valid id',
                'status':ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST) 
    # default case
    response_data = {
                    'result': 'Method not allowed',
                    'status': ResponseStatus.FAIL.value
                    }           
    return Response(response_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)