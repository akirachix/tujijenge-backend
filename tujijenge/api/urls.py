from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  PaymentViewSet, OrderViewSet, CommunityViewSet, CommunityMembersViewSet, TrainingSessionsViewSet, TrainingRegistrationViewSet,ProductViewSet, StockViewSet
from .views import UnifiedUserViewSet

router =DefaultRouter()

router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"community", CommunityViewSet, basename="community")
router.register(r"community_members", CommunityMembersViewSet, basename="community_members")
router.register(r"training_sessions", TrainingSessionsViewSet, basename="training_sessions")
router.register(r"training_registration", TrainingRegistrationViewSet, basename="training_registration")
router.register(r'products', ProductViewSet, basename='product')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'user', UnifiedUserViewSet, basename='user')


urlpatterns = [
    path("", include(router.urls)),

]











