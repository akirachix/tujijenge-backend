from rest_framework import serializers
from users.models import Mamamboga
from users.models import Stakeholder
from payments.models import Order
from payments.models import Payment


class MamambogaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Mamamboga
        fields ="__all__"

class StakeholderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Stakeholder
        fields ="__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields ="__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields ="__all__"


        