from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewDetailsSerializer, ReviewSerializer
from core.ResponseStatus import ResponseStatus
from django.utils import timezone
from user.permission import IsAuthenticatedUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
import logging
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


logger = logging.getLogger("review")
# Create your views here.
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewDetailsSerializer
    permission_classes=[IsAuthenticatedUser]
    authentication_classes=[JWTAuthentication]
    lookup_field = 'id'

    def get_queryset(self):
        return Review.objects.all()
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def get_all_reviews(self, request, *args, **kwargs):
        reviews = self.get_queryset()
        serializer = ReviewSerializer(reviews, many=True)
        return Response({
            'result': serializer.data,
            'status': ResponseStatus.SUCCESS.value
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='user_reviews/(?P<user_id>[^/.]+)', permission_classes=[IsAuthenticatedUser])
    def get_reviews_user_id(self, request, user_id, *args, **kwargs):
        try:
            reviews = self.get_queryset().filter(user_id=user_id)

            if not reviews.exists():
                response_data = {
                    'error': "No reviews found by this user",
                    'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(reviews, many=True)
            response_data = {
                'result': serializer.data,
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_data = {
                'error': str(e),
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedUser])
    def get_reviews_pujo_id(self, request, pujo_id, *args, **kwargs):

        try:
            reviews = self.get_queryset().filter(pujo_id=pujo_id)

            if not reviews.exists():
                response_data = {
                    'error': "No reviews found for this pujo",
                    'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(reviews, many=True)
            response_data = {
                'result': serializer.data,
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_data = {
                'error': str(e),
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def retrieve(self, request, uuid=None,*args, **kwargs):
        try:
            user = request.user
            self.check_object_permissions(request, user)
            review = self.get_queryset().filter(id=uuid).first()
            if review is None:
                response_data = {
                'result': 'Given Review does not exist',
                'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(review)
            response_data = {
                'result':serializer.data,
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            response_data = {
                'result': 'Given Pujo does not exist',
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        self.check_permissions(request, user)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'result': serializer.data,
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'error': serializer.errors,
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, uuid=None, *args, **kwargs):
        try:
            user = request.user
            self.check_object_permissions(request, user)
            review = self.get_queryset().filter(id=uuid).first()

            if not review:
                response_data={
                    'error':"Review does not exist",
                    'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(edited_at=timezone.now())
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
        except Review.DoesNotExist:
            response_data = {
                'result': 'Given review does not exist',
                'status': ResponseStatus.FAIL.value
                 }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, uuid=None, *args, **kwargs):
        try:
            user = request.user
            self.check_object_permissions(request, user)
            review = self.get_queryset().filter(id=uuid).first()
            if review is None:
                response_data = {
                'error': 'Given Review does not exist',
                'status': ResponseStatus.FAIL.value
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            
            review.delete()
            response_data = {
                'result': "Delete successful",
                'status': ResponseStatus.SUCCESS.value
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            response_data = {
                'error': 'Given Review does not exist',
                'status': ResponseStatus.FAIL.value
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)