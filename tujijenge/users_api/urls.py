from django.urls import path
from .views import UserPolymorphicCRUDView

urlpatterns = [
    path('users/', UserPolymorphicCRUDView.as_view(), name='users-crud-all'),  # GET (all), POST
    path('users/<str:pk>/', UserPolymorphicCRUDView.as_view(), name='users-crud-detail'),  # GET (single), PUT, PATCH, DELETE
]