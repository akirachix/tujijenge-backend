from rest_framework import serializers
from orders.models import Order
from stock.models import  Product, Stock
from communities.models import Community, CommunityMembers, TrainingSessions, TrainingRegistration
from users.models import Mamamboga, Stakeholder

class MamambogaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mamamboga
        fields = "__all__"

class StakeholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stakeholder
        fields = "__all__"

class CommunitySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Community
        fields = "__all__"

class CommunityMembersSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CommunityMembers
        fields = "__all__"
        
class TrainingSessionsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TrainingSessions
        fields = "__all__"
        
class TrainingRegistrationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TrainingRegistration
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields ="__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"
    def validate(self, data):
        if data.get('price') is not None and data['price'] < 0:
            raise serializers.ValidationError({"price": "Price cannot be negative."})
        if data.get('quantity') is not None and data['quantity'] < 0:
            raise serializers.ValidationError({"quantity": "Quantity cannot be negative."})
        return data

class STKPushSerializer(serializers.Serializer):
   phone_number = serializers.CharField()
   amount = serializers.DecimalField(max_digits=10, decimal_places=2)
   cart_item = serializers.ListField()
   account_reference = serializers.CharField()
   transaction_desc = serializers.CharField()