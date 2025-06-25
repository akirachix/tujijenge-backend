from rest_framework import serializers
from stock.models import Category, Tag, Product, Stock
from users.models import Mamamboga

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields= "__all__"
 
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model=Stock
        fields= "__all__"




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [ 'name']
