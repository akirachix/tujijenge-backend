from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, StockViewSet

router=DefaultRouter()
router.register(r"product", ProductViewSet, basename='products')
router.register(r"stock", StockViewSet, basename='stocks')
urlpatterns=[path("",include(router.urls))]