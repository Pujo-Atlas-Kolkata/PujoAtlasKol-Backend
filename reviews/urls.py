from django.urls import path
from .views import ReviewViewSet

review_create = ReviewViewSet.as_view({
    'post':'create'
})

review_details = ReviewViewSet.as_view({
    'get': 'retrieve',    # Retrieve action
    'patch': 'partial_update',      # patch action
    'delete': 'destroy'   # Delete action
})

urlpatterns = [
    path('list', ReviewViewSet.as_view({'get':"get_all_reviews"}), name='all_reviews'),
    path('create', review_create, name="review-create"),
    path('<uuid:uuid>', review_details, name="review_details"),
    path('user_reviews/<uuid:user_id>', ReviewViewSet.as_view({'get':"get_reviews_user_id"}), name="reviews-user"),
    path('pujo_reviews/<uuid:pujo_id>', ReviewViewSet.as_view({'get':"get_reviews_pujo_id"}), name="reviews-pujo"),
]