from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UnifiedUserViewSet

router = DefaultRouter()
router.register(r'user', UnifiedUserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]