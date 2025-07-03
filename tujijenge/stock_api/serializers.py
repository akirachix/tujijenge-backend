from rest_framework import serializers
from stock.models import  Product, Stock


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