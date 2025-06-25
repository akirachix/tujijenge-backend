from django.shortcuts import render
from rest_framework import viewsets
from users.models import Mamamboga, Stakeholder
from .serializers import MamambogaSerializer, StakeholderSerializer,CommunitySerializer, CommunityMembersSerializer, TrainingSessionsSerializer, TrainingRegistrationSerializer
from communities.models import Community, CommunityMembers, TrainingSessions, TrainingRegistration



class MamambogaViewSet(viewsets.ModelViewSet):
    queryset = Mamamboga.objects.all()
    serializer_class=MamambogaSerializer

class StakeholderViewSet(viewsets.ModelViewSet):
    queryset = Stakeholder.objects.all()
    serializer_class=StakeholderSerializer
    
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
    
    

