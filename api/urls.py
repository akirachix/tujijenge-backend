from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  OrderViewSet, CommunityViewSet, CommunityMembersViewSet, TrainingSessionsViewSet, TrainingRegistrationViewSet,ProductViewSet, StockViewSet,STKPushView, daraja_callback
from .views import UnifiedUserViewSet

router =DefaultRouter()


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
    path('daraja/stk-push/', STKPushView.as_view(), name='daraja-stk-push'),
    path('daraja/callback/', daraja_callback, name='daraja-callback'),
]












