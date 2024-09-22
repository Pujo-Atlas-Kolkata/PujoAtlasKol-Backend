from django.urls import path
from .views import UserViewSet, FavoritesViewSet, WishlistViewSet, SaveViewSet

# Define custom views for list and detail actions
# app_name = 'user'

user_create = UserViewSet.as_view({
    'post': 'create'  # Create action
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',    # Retrieve action
    'put': 'update',      # Update action
    'delete': 'destroy',   # Delete action
    'patch':'partial_update' # patch action
})

favorities_create = FavoritesViewSet.as_view({'post': 'add_favorite'})
favorites_remove = FavoritesViewSet.as_view({'post': 'remove_favorite'})

wishlist_create = WishlistViewSet.as_view({'post': 'add_wishlist'})
wishlist_remove = WishlistViewSet.as_view({'post': 'remove_wishlist'})

saved_add = SaveViewSet.as_view({'post':'add_saved'})
saved_remove = SaveViewSet.as_view({'post':'remove_saved'})

urlpatterns = [
    path('register', user_create, name='user_create'),  # URL for creating a new User
    path('<uuid:uuid>', user_detail, name='user_detail'),  # URL for detail, update, and delete
    path('<uuid:user_id>/favorites/add',favorities_create,name="favs_create"),
    path('<uuid:user_id>/favorites/remove', favorites_remove, name="fav_remove"),
    path('<uuid:user_id>/wishlist/add', wishlist_create, name="wishlist_create"),
    path('<uuid:user_id>/wishlist/remove', wishlist_remove, name="wishlist_remove"),
    path('<uuid:user_id>/save/remove', saved_add, name="saved_remove"),
    path('<uuid:user_id>/save/remove', saved_remove, name="saved_remove"),
]
