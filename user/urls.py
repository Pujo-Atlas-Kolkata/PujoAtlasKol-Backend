from django.urls import path
from .views import UserViewSet, FavoritesViewSet, WishlistViewSet, SaveViewSet, PandalVisitsViewSet

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

pandal_visits_add = PandalVisitsViewSet.as_view({'post':'add_visits'})
pandal_visits_remove = PandalVisitsViewSet.as_view({'post':'remove_visits'})

urlpatterns = [
    path('register', user_create, name='user_create'),  # URL for creating a new User
    path('<uuid:uuid>', user_detail, name='user_detail'),  # URL for detail, update, and delete
    path('favorites/add',favorities_create,name="favs_create"),
    path('favorites/remove', favorites_remove, name="fav_remove"),
    path('wishlist/add', wishlist_create, name="wishlist_create"),
    path('wishlist/remove', wishlist_remove, name="wishlist_remove"),
    path('save/add', saved_add, name="saved_add"),
    path('save/remove', saved_remove, name="saved_remove"),
    path('pandal_visits/add', pandal_visits_add, name="pandal_visits_add"),
    path('user_details/<uuid:user_id>', UserViewSet.as_view({'get':'get_user_details'}), name='get_user_details')
]
