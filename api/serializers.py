from rest_framework import serializers
from orders.models import Order
from stock.models import  Product, Stock
from communities.models import Community, CommunityMembers, TrainingSessions, TrainingRegistration
from users.models import Mamamboga, Stakeholder
from cart.models import Cart, CartItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class MamambogaSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(write_only=True)

    class Meta:
        model = Mamamboga
        fields = ['id', 'pin', 'first_name', 'last_name', 'phone_number', 'latitude', 'longitude', 'address', 'image', 'is_active', 'deactivation_date', 'certified_status', 'created_at', 'updated_at']

    def create(self, validated_data):
        pin = validated_data.pop("pin")
        phone = validated_data.get("phone_number")
        username = phone.replace("+", "")
        password = pin
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        mamamboga = Mamamboga.objects.create(user=user, pin=pin, **validated_data)
        return mamamboga

class StakeholderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Stakeholder
        fields = [
            'id', 'user', 'first_name', 'last_name', 'role', 'created_at'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        stakeholder = Stakeholder.objects.create(
            user=user,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'Supplier'),
            stakeholder_email=user_data['email'],        
            password_hash=user_data['password'],        
        )
        return stakeholder

class CommunitySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Community
        fields = "__all__"

class CommunityMembersSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CommunityMembers
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CartItem
        fields = "__all__"
        
class CartSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Cart
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