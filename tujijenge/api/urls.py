from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MamambogaViewSet, StakeholderViewSet, PaymentViewSet, OrderViewSet

router =DefaultRouter()
router.register(r"MamaMbogas", MamambogaViewSet, basename="mamambogas")
router.register(r"Stakeholder", StakeholderViewSet, basename="stakeholders")
router.register(r"Payment", PaymentViewSet, basename="payments")
router.register(r"Order", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]