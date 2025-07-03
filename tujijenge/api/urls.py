from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  PaymentViewSet, OrderViewSet


router =DefaultRouter()

router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"orders", OrderViewSet, basename="orders")


urlpatterns = [
    path("", include(router.urls)),
]