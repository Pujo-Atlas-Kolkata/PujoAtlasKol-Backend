from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Transport
from .serializers import TransportSerializer
from core.ResponseStatus import ResponseStatus
import logging
from user.permission import IsSuperOrAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
import re
from django.utils import timezone
from django.db.models.functions import Coalesce, Cast
from datetime import datetime

logger = logging.getLogger("transport")

class TransportViewSet(viewsets.ModelViewSet):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer
    lookup_field = 'id'
    permission_classes=[IsSuperOrAdminUser]
    authentication_classes=[JWTAuthentication]

    def get_permissions(self):
        if self.action in ['list']:
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                    'result': serializer.data,
                    'message':'List successfully fetched',
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
        
    def create(self, request, *args, **kwargs):
        user = request.user
        self.check_object_permissions(request, user)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'result': {'id': serializer.data["id"]},
                'message':'Transport created',
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
    
    def destroy(self, request, *args, uuid=None, **kwargs):
        try:
            user = request.user
            self.check_object_permissions(request, user)
            transport = self.get_queryset().filter(id=uuid).first()
            if transport is None:
                response_data = {
                'error': 'Given Transport does not exist',
                'status': ResponseStatus.FAIL.value
                }
                user_id = request.user.id if request.user.is_authenticated else None
                logger.error(f"Error: {response_data['error']}", extra={'user_id': user_id})
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
            transport.delete()
            response_data = {
                'result': f"Delete successful for {str(uuid)}",
                'status': ResponseStatus.SUCCESS.value
            }
            user_id = request.user.id if request.user.is_authenticated else None
            logger.info(f"Success: {response_data['result']}", extra={'user_id': user_id})
            return Response(response_data, status=status.HTTP_200_OK)
        except Transport.DoesNotExist:
            response_data = {
                'error': 'Given Transport does not exist',
                'status': ResponseStatus.FAIL.value
                }
            user_id = request.user.id if request.user.is_authenticated else None
            logger.error(f"Error: {response_data['error']}", extra={'user_id': user_id})
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)