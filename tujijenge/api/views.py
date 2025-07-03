from django.shortcuts import render
from rest_framework import viewsets

from payments.models import Payment, Order

from .serializers import PaymentSerializer,OrderSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer




