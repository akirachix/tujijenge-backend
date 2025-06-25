from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MamambogaViewSet, StakeholderViewSet

router =DefaultRouter()
router.register(r"MamaMbogas", MamambogaViewSet, basename="mamambogas")
router.register(r"Stakeholder", StakeholderViewSet, basename="stakeholders")

urlpatterns = [
    path("", include(router.urls)),
]