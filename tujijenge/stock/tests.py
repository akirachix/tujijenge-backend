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

class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

        self.url = reverse('product-list')  # /api/products/

        self.valid_data = {
            "product_name": "Bananas",
            "unit": "kg",
            "product_price": "30.00",
            "category": "VEG"
        }

    def test_create_product(self):
        """Test creating a product via API."""
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product_name'], "Bananas")
        self.assertEqual(response.data['category'], "VEG")

    def test_list_products(self):
        """Test retrieving a list of products via API."""
        Product.objects.create(
            product_name="Pineapple",
            unit="pcs",
            product_price=50.00,
            category="VEG"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_product_detail(self):
        """Test retrieving a specific product via API."""
        product = Product.objects.create(
            product_name="Mango",
            unit="pcs",
            product_price=40.00,
            category="VEG"
        )
        url = reverse('product-detail', kwargs={'pk':product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_name'], "Mango")

    def test_update_product(self):
        """Test updating a product via API."""
        product = Product.objects.create(
            product_name="Papaya",
            unit="pcs",
            product_price=60.00,
            category="VEG"
        )
        url = reverse('product-detail', kwargs={'pk':product.pk})
        updated_data = {
            "product_name": "Papaya (Updated)",
            "unit": "pcs",
            "product_price": "65.00",
            "category": "VEG"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_name'], "Papaya (Updated)")

    def test_delete_product(self):
        """Test deleting a product via API."""
        product = Product.objects.create(
            product_name="Orange",
            unit="pcs",
            product_price=20.00,
            category="VEG"
        )
        url = reverse('product-detail', kwargs={'pk':product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=product.pk).exists())

    def test_invalid_product_data(self):
        """Test creating a product with invalid data."""
        bad_data = {
            "product_name": "Invalid Product",
            "unit": "kg",
            "product_price": "-10.00",  # Invalid: negative
            "category": "VEG"
        }
        response = self.client.post(self.url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class StockAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            email="john@example.com",
            password="password123"
        )
        self.client.force_authenticate(user=self.user)

        self.url = reverse('stock-list')  # /api/stocks/

        self.valid_data = {
            "price": "120.00",
            "quantity": "15.00",
            "expiration_date": timezone_now().isoformat()
        }

    def test_create_stock(self):
        """Test creating a stock entry via API."""
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['price']), 120.00)

    def test_list_stocks(self):
        """Test retrieving a list of stock entries via API."""
        Stock.objects.create(
            price=100.00,
            quantity=10.00
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_stock_detail(self):
        """Test retrieving a specific stock entry via API."""
        stock = Stock.objects.create(
            price=80.00,
            quantity=5.00
        )
        url = reverse('stock-detail', kwargs={'pk':stock.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['price']), 80.00)

    def test_update_stock(self):
        """Test updating a stock entry via API."""
        stock = Stock.objects.create(
            price=75.00,
            quantity=4.00
        )
        url = reverse('stock-detail', kwargs={'pk':stock.pk})
        updated_data = {
            "price": "90.00",
            "quantity": "8.00"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['price']), 90.00)

    def test_delete_stock(self):
        """Test deleting a stock entry via API."""
        stock = Stock.objects.create(
            price=70.00,
            quantity=3.00
        )
        url = reverse('stock-detail', kwargs={'pk':stock.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_stock_data(self):
        """Test creating a stock entry with invalid data."""
        bad_data = {
            "price": "-100.00",  # Invalid: negative
            "quantity": "-5.00"  # Invalid: negative
        }
        response = self.client.post(self.url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

