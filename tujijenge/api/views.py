from django.shortcuts import render
from rest_framework import viewsets
from users.models import Mamamboga, Stakeholder
from payments.models import Payment, Order
from .serializers import MamambogaSerializer, StakeholderSerializer,PaymentSerializer,OrderSerializer



class MamambogaViewSet(viewsets.ModelViewSet):
    queryset = Mamamboga.objects.all()
    serializer_class=MamambogaSerializer

class StakeholderViewSet(viewsets.ModelViewSet):
    queryset = Stakeholder.objects.all()
    serializer_class=StakeholderSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

