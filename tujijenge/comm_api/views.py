from django.shortcuts import render
from rest_framework import viewsets # type: ignore
from .serializers import CommunitySerializer, CommunityMembersSerializer, TrainingSessionsSerializer, TrainingRegistrationSerializer
from communities.models import Community, CommunityMembers, TrainingSessions, TrainingRegistration

# Create your views here.
class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class=CommunitySerializer
    
class CommunityMembersViewSet(viewsets.ModelViewSet):
    queryset = CommunityMembers.objects.all()
    serializer_class=CommunityMembersSerializer
    
class TrainingSessionsViewSet(viewsets.ModelViewSet):
    queryset = TrainingSessions.objects.all()
    serializer_class=TrainingSessionsSerializer
    
class TrainingRegistrationViewSet(viewsets.ModelViewSet):
    queryset = TrainingRegistration.objects.all()
    serializer_class=TrainingRegistrationSerializer
    