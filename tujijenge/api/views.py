from django.shortcuts import render
from rest_framework import viewsets
from users.models import Mamamboga, Stakeholder
from stock.models import Product,Stock
from .serializers import MamambogaSerializer, StakeholderSerializer
from .serializers import ProductSerializer, StockSerializer

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
