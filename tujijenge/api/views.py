from django.shortcuts import render
from rest_framework import viewsets
from users.models import Mamamboga, Stakeholder

from stock.models import Product,Stock

from .serializers import MamambogaSerializer, StakeholderSerializer,CommunitySerializer, CommunityMembersSerializer, TrainingSessionsSerializer, TrainingRegistrationSerializer, MamambogaSerializer, StakeholderSerializer, ProductSerializer, StockSerializer
from communities.models import Community, CommunityMembers, TrainingSessions, TrainingRegistration




class MamambogaViewSet(viewsets.ModelViewSet):
    queryset = Mamamboga.objects.all()
    serializer_class=MamambogaSerializer

class StakeholderViewSet(viewsets.ModelViewSet):
    queryset = Stakeholder.objects.all()
    serializer_class=StakeholderSerializer
class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset=Stock.objects.all()
    serializer_class = StockSerializer

    
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
    
    


