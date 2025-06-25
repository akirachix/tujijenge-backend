from django.urls import path, include
from rest_framework.routers import DefaultRouter # type: ignore

from .views import CommunityViewSet, CommunityMembersViewSet, TrainingSessionsViewSet, TrainingRegistrationViewSet

router = DefaultRouter()
router.register(r"community", CommunityViewSet, basename="community")
router.register(r"community_members", CommunityMembersViewSet, basename="community_members")
router.register(r"training_sessions", TrainingSessionsViewSet, basename="training_sessions")
router.register(r"training_registration", TrainingRegistrationViewSet, basename="training_registration")

urlpatterns = [
    path("", include(router.urls)),
]