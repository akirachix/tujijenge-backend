from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.timezone import now as timezone_now
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

from stock.models import Product, Stock
class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            product_name="Bananas",
            unit="kg",
            product_price=30.00,
            category="VEG"
        )

    def test_product_str(self):
        """Test Product string representation."""
        self.assertEqual(str(self.product), "Bananas")

    def test_product_creation(self):
        """Test creating a Product instance."""
        product = Product.objects.create(

            product_name="Apples",
            unit="kg",
            product_price=40.00,
            category="VEG"
        )
        self.assertEqual(product.product_name, "Apples")
        self.assertEqual(Product.objects.count(), 2)

    def test_product_price_validation(self):
        """Test that negative product_price raises ValidationError."""
        product = Product(
            product_name="Mangoes",
            unit="kg",
            product_price=-10.00,
            category="VEG"
        )
        with self.assertRaises(ValidationError):
            product.full_clean()



class StockModelTest(TestCase):
    def setUp(self):
        self.stock = Stock.objects.create(
            price=120.00,
            quantity=15.00,
            expiration_date=timezone_now()
        )



    def test_stock_creation(self):
        """Test creating a Stock instance."""
        stock = Stock.objects.create(
            price=100.00,
            quantity=10.00
        )
        self.assertEqual(stock.price, 100.00)
        self.assertEqual(Stock.objects.count(), 2)