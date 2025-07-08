
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.timezone import now as timezone_now
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

from stock.models import Product, Stock
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Mamamboga, Stakeholder

class UnifiedUserViewSetTests(APITestCase):
    def setUp(self):
        self.mamamboga = Mamamboga.objects.create(
            first_name="Mamu",
            last_name="Boga",
            pin="1234"
        )
        self.stakeholder = Stakeholder.objects.create(
            first_name="Stake",
            last_name="Holder",
            stakeholder_email="stake@example.com",
            password_hash="abcd"
        )

    def test_list_all_users(self):
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [u['first_name'] for u in response.data]
        self.assertIn("Mamu", names)
        self.assertIn("Stake", names)

    def test_list_mamamboga(self):
        response = self.client.get('/api/user/?user_type=mamamboga')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for entry in response.data:
            self.assertNotIn('stakeholder_email', entry)

    def test_list_stakeholder(self):
        response = self.client.get('/api/user/?user_type=stakeholder')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for entry in response.data:
            self.assertIn('stakeholder_email', entry)

    def test_retrieve_mamamboga(self):
        response = self.client.get(f'/api/user/{self.mamamboga.pk}/?user_type=mamamboga')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Mamu")


    def test_retrieve_stakeholder(self):
        response = self.client.get(f'/api/user/{self.stakeholder.pk}/?user_type=stakeholder')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Stake")
        self.assertEqual(response.data['stakeholder_email'], "stake@example.com")

    def test_create_stakeholder(self):
        data = {
            "user_type": "stakeholder",
            "first_name": "Jane",
            "last_name": "Doe",
            "stakeholder_email": "janedoe@example.com",
            "password_hash": "mypassword"
        }
        response = self.client.post('/api/user/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], "Jane")
        self.assertEqual(response.data['stakeholder_email'], "janedoe@example.com")


    def test_delete_mamamboga(self):
        response = self.client.delete(f'/api/user/{self.mamamboga.pk}/?user_type=mamamboga')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Mamamboga.objects.filter(pk=self.mamamboga.pk).exists())

    def test_delete_stakeholder(self):
        response = self.client.delete(f'/api/user/{self.stakeholder.pk}/?user_type=stakeholder')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Stakeholder.objects.filter(pk=self.stakeholder.pk).exists())



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
