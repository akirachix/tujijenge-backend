from django.shortcuts import render
from rest_framework import viewsets
from users.models import Mamamboga, Stakeholder
from .serializers import MamambogaSerializer, StakeholderSerializer


class MamambogaViewSet(viewsets.ModelViewSet):
    queryset = Mamamboga.objects.all()
    serializer_class=MamambogaSerializer

class StakeholderViewSet(viewsets.ModelViewSet):
    queryset = Stakeholder.objects.all()
    serializer_class=StakeholderSerializer
