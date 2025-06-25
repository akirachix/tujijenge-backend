from rest_framework import serializers
from stock.models import Category, Tag, Product, Stock
from users.models import Mamamboga

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class MamambogaSerializer(serializers.ModelSerializer):
    mamamboga_name = serializers.SerializerMethodField()

    class Meta:
        model = Mamamboga
        fields = ['id', 'mamamboga_name']

    def get_mamamboga_name(self, obj):
        return f"{obj.first_name} {obj.last_name or ''}".strip()

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source='tags', many=True, write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            'product_id', 'product_name', 'unit', 'category', 'category_id',
            'description', 'product_price', 'created_at', 'tags', 'tag_ids'
        ]

class StockSerializer(serializers.ModelSerializer):
    mamamboga = MamambogaSerializer(read_only=True)
    mamamboga_id = serializers.PrimaryKeyRelatedField(
        queryset=Mamamboga.objects.all(), source='mamamboga', write_only=True, allow_null=True
    )

    class Meta:
        model = Stock
        fields = [
            'stock_id', 'mamamboga', 'mamamboga_id', 'price', 'quantity',
            'last_updated', 'expiration_date', 'last_sync_at', 'created_at'
        ]