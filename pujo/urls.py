from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.getPujoList),
    path('<uuid:pk>/', views.getPujoDetail),
    path('create/', views.addNewPujo),
    path('update/<uuid:pk>/',views.updatePujoDetails),
    path('delete/<uuid:pk>/',views.DeletePujo),
]
