from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MamambogaViewSet, StakeholderViewSet, ProductViewSet, StockViewSet

router =DefaultRouter()
router.register(r"MamaMbogas", MamambogaViewSet, basename="mamambogas")
router.register(r"Stakeholder", StakeholderViewSet, basename="stakeholders")
router.register(r"products", ProductViewSet, basename='product')
router.register(r"stocks", StockViewSet, basename='stock')

urlpatterns = [
    path("", include(router.urls)),
]