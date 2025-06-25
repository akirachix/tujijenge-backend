from rest_framework import serializers



from payments.models import Order
from payments.models import Payment






class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields ="__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields ="__all__"




