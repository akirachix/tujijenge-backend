from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MamambogaViewSet, StakeholderViewSet , CommunityViewSet, CommunityMembersViewSet, TrainingSessionsViewSet, TrainingRegistrationViewSet


router =DefaultRouter()
router.register(r"MamaMbogas", MamambogaViewSet, basename="mamambogas")
router.register(r"Stakeholder", StakeholderViewSet, basename="stakeholders")
router.register(r"Community", CommunityViewSet, basename="communities")
router.register(r"CommunityMembers", CommunityMembersViewSet, basename="communitymembers")
router.register(r"TrainingSessions", TrainingSessionsViewSet, basename="trainingsessions")
router.register(r"TrainingRegistration", TrainingRegistrationViewSet, basename="trainingregistration")

urlpatterns = [
    path("", include(router.urls)),
]