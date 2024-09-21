from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F
from .models import User
from .serializers import UserSerializer
from core.ResponseStatus import ResponseStatus
import logging
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from .permission import IsAuthenticatedUser

logger = logging.getLogger("user")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedUser]
        
    def retrieve(self, request, uuid, *args, **kwargs):
        try:
            self.check_permissions(request)   
            user = self.get_queryset().filter(id=uuid).first()
            if not user:
                response_data={
                'error':"User does not exist",
                'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            else:
                serializer = self.get_serializer(user)
                response_data = {
                    'result':serializer.data,
                    'status':ResponseStatus.SUCCESS.value
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            response_data = {
                'result':'User does not exist',
                'status':ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request, *args, **kwargs):
        try:
            self.check_permissions(request)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response_data={
                    'result':{'id':serializer.data["id"]},
                    'status':ResponseStatus.SUCCESS.value
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data={
                    'error':serializer.errors,
                    'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:  # Catch any other unexpected exceptions
            response_data = {
                'result': str(e),
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, uuid=None, *args, **kwargs):
        self.check_permissions(request)
        user = self.get_queryset().filter(id=uuid).first()
        if not user:
            response_data = {
                'error': "User does not exist",
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        
        # Pass the data to the serializer
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
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

        
    def destroy(self, request, uuid=None, *args, **kwargs):
        self.check_permissions(request)
        user = self.get_queryset().filter(id=uuid).first()

        if not user:
            response_data={
                'error':"User does not exist",
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        else:
            user.delete()

            response_data = {
                'result': 'User deleted successfully',
                'status': 'success'
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, uuid=None, *args, **kwargs):
        try:
            self.check_permissions(request)
            user = self.get_queryset().filter(id=uuid).first()
            
            if not user:
                response_data={
                    'error':"User does not exist",
                    'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            else:
                serializer = self.get_serializer(user, data=request.data, partial=True)
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
        except User.DoesNotExist:
            response_data = {
                'result': 'Given user does not exist',
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                response_data = {
                    'result': 'Logged in successfully',
                    'status': ResponseStatus.SUCCESS.value
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                'error': 'Invalid credentials',
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        else:
            response_data = {
                'error': 'Invalid credentials',
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        response_data = {
                'result': 'Logged out successfully',
                'status': ResponseStatus.SUCCESS.value
                }
        return Response(response_data, status=status.HTTP_200_OK)
