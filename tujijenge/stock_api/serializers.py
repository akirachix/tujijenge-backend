from rest_framework import serializers
from stock.models import  Product, Stock


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'product_id', 'product_name', 'unit', 'category', 
            'product_price', 'created_at'
        ]

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            'stock_id', 'price', 'quantity',
            'last_updated', 'expiration_date', 'last_sync_at', 'created_at'
        ]