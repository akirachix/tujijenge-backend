from rest_framework import serializers
from users.models import Mamamboga
from users.models import Stakeholder
from stock.models import Product, Stock

class MamambogaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Mamamboga
        fields ="__all__"

class StakeholderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Stakeholder
        fields ="__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields= "__all__"
 
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model=Stock
        fields= "__all__"
