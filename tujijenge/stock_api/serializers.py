from rest_framework import serializers
from stock.models import  Product, Stock
# from users.models import Mamamboga


# class MamambogaSerializer(serializers.ModelSerializer):
#     mamamboga_name = serializers.SerializerMethodField()

    # class Meta:
    #     model = Mamamboga
    #     fields = ['id', 'mamamboga_name']

    # def get_mamamboga_name(self, obj):
    #     return f"{obj.first_name} {obj.last_name or ''}".strip()

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'product_id', 'product_name', 'unit', 'category', 
            'product_price', 'created_at'
        ]

class StockSerializer(serializers.ModelSerializer):
    # mamamboga = MamambogaSerializer(read_only=True)
    # mamamboga_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Mamamboga.objects.all(), source='mamamboga', write_only=True, allow_null=True
    # )

    class Meta:
        model = Stock
        fields = [
            'stock_id', 'price', 'quantity',
            'last_updated', 'expiration_date', 'last_sync_at', 'created_at'
        ]