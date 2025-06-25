from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone

from stock.models import Category, Tag, Product, Stock
from users.models import Mamamboga 

class ProductAPITest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fruits")
        self.tag = Tag.objects.create(name="Organic")
        self.url = reverse('product-list')  

        self.valid_data = {
            "product_id": "P001",
            "product_name": "Bananas",
            "unit": "kg",
            "category": self.category.id,
            "product_price": "30.00",
            "description": "Sweet bananas",
            "tags": [self.tag.id]
        }

    def test_create_product(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_products(self):
        Product.objects.create(
            product_id="P002",
            product_name="Pineapple",
            unit="pcs",
            category=self.category,
            product_price="50.00"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_product(self):
        product = Product.objects.create(
            product_id="P003",
            product_name="Mango",
            unit="pcs",
            category=self.category,
            product_price="40.00"
        )
        url = reverse('product-detail', args=[product.pk])
        updated_data = {
            "product_id": "P003",
            "product_name": "Mango (Updated)",
            "unit": "pcs",
            "category": self.category.id,
            "product_price": "45.00"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_name'], "Mango (Updated)")

    def test_delete_product(self):
        product = Product.objects.create(
            product_id="P004",
            product_name="Papaya",
            unit="pcs",
            category=self.category,
            product_price="60.00"
        )
        url = reverse('product-detail', args=[product.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_product_data(self):
        bad_data = {
            "product_id": "",  # required field
            "product_price": -10  # invalid value
        }
        response = self.client.post(self.url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class StockAPITest(APITestCase):
    def setUp(self):
        self.mamamboga = Mamamboga.objects.create(
            mamamboga_id="M001",
            mamamboga_name="Mama Asha",
            phone_number="0712345678",
            pin="1234"
        )
        self.url = reverse('stock-list')
        self.valid_data = {
            "stock_id": "S001",
            "mamamboga": self.mamamboga.mamamboga_id,
            "price": "120.00",
            "quantity": "15.0",
            "expiration_date": timezone.now().isoformat()
        }

    def test_create_stock(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_stocks(self):
        Stock.objects.create(
            stock_id="S002",
            mamamboga=self.mamamboga,
            price=100.00,
            quantity=10.0
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_stock(self):
        stock = Stock.objects.create(
            stock_id="S003",
            mamamboga=self.mamamboga,
            price=80.00,
            quantity=5.0
        )
        url = reverse('stock-detail', args=[stock.pk])
        updated_data = {
            "stock_id": "S003",
            "mamamboga": self.mamamboga.mamamboga_id,
            "price": "90.00",
            "quantity": "8.0"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], "90.00")

    def test_delete_stock(self):
        stock = Stock.objects.create(
            stock_id="S004",
            mamamboga=self.mamamboga,
            price=75.00,
            quantity=4.0
        )
        url = reverse('stock-detail', args=[stock.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_stock_data(self):
        bad_data = {
            "stock_id": "",
            "mamamboga": "",
            "price": -100,
            "quantity": -5
        }
        response = self.client.post(self.url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
