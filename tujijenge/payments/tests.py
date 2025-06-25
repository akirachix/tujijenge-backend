from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from payments.models import Order, Payment
from users.models import Mamamboga, Stakeholder
from stock.models import Product, Category
from communities.models import Community
from django.utils import timezone

class PaymentAPITestCase(APITestCase):
    def setUp(self):
    
        self.mamamboga = Mamamboga.objects.create(
            id="m001",
            first_name="Akeza",
            last_name="Saloi",
            phone_number="+254780300748",
            pin="1234",
            latitude=36.6678,
            longitude=36.6678,
            is_active=True,
            deactivation_date=timezone.now(),
            certified_status="In Training"
        )
        self.stakeholder = Stakeholder.objects.create(
            id="S001",
            first_name="Saloi",
            last_name="Stake",
            phone_number="+254780300700",
            stakeholder_email="aksaloi@gmail.com",
            password_hash="Akezasaloi"
        )
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            product_id="P0011",
            product_name="Test Product",
            product_price=1000.00,
            unit="kg",
            category=self.category,
            description="Fresh from the farm"
        )
        self.community = Community.objects.create(
            community_id="C001",
            name="Test Community",
            description="A Community built on trust",
            latitude=36.6678,
            longitude=36.6678,
            created_by=self.mamamboga
        )
        self.order = Order.objects.create(
            order_id="O001",
            mamamboga=self.mamamboga,
            product=self.product,
            community=self.community,
            quantity=3,
            total_price=1500.00,
            deadline_at=timezone.now(),
            order_date=timezone.now()
        )

    def test_create_payment(self):
        url = reverse('payments-list')
        data = {
            "payment_id": "P0001",
            "order": self.order.order_id,
            "amount": "1500.00",
            "receiver": self.stakeholder.id,
            "status": "pending",
            "payment_date": timezone.now().isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(response.data['amount'], "1500.00")

    def test_list_payments(self):
        Payment.objects.create(
            payment_id="P0002",
            order=self.order,
            amount=500.00,
            receiver=self.stakeholder,
            status="completed",
            payment_date=timezone.now()
        )
        url = reverse('payments-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertTrue(isinstance(response.data, list) or 'results' in response.data)

    def test_retrieve_payment(self):
        payment = Payment.objects.create(
            payment_id="P0003",
            order=self.order,
            amount=500.00,
            receiver=self.stakeholder,
            status="completed",
            payment_date=timezone.now()
        )
        url = reverse('payments-detail', args=[payment.payment_id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], "500.00")

    def test_update_payment(self):
        payment = Payment.objects.create(
            payment_id="P0004",
            order=self.order,
            amount=500.00,
            receiver=self.stakeholder,
            status="pending",
            payment_date=timezone.now()
        )
        url = reverse('payments-detail', args=[payment.payment_id])
        data = {
            "payment_id": payment.payment_id,
            "order": self.order.order_id,
            "amount": "700.00",
            "receiver": self.stakeholder.id,
            "status": "completed",
            "payment_date": timezone.now().isoformat()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment.refresh_from_db()
        self.assertEqual(str(payment.amount), "700.00")

    def test_delete_payment(self):
        payment = Payment.objects.create(
            payment_id="P0005",
            order=self.order,
            amount=500.00,
            receiver=self.stakeholder,
            status="completed",
            payment_date=timezone.now()
        )
        url = reverse('payments-detail', args=[payment.payment_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Payment.objects.filter(payment_id=payment.payment_id).exists())

class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            product_id="P0011",
            product_name="Test Product",
            product_price=1000.00,
            unit="kg",
            category=self.category,
            description="Fresh from the farm"
        )
        self.mamamboga = Mamamboga.objects.create(
            id="m001",
            first_name="Akeza",
            last_name="Saloi",
            phone_number="+254780300748",
            pin="1234",
            latitude=36.6678,
            longitude=36.6678,
            is_active=True,
            deactivation_date=timezone.now(),
            certified_status="In Training"
        )
        self.community = Community.objects.create(
            community_id="C001",
            name="Test Community",
            description="A Community built on trust",
            latitude=36.6678,
            longitude=36.6678,
            created_by=self.mamamboga
        )
        self.order = Order.objects.create(
            order_id="O001",
            mamamboga=self.mamamboga,
            product=self.product,
            community=self.community,
            quantity=3,
            total_price=1500.00,
            deadline_at=timezone.now(),
            order_date=timezone.now()
        )

    def test_create_order(self):
        url = reverse('orders-list')
        data = {
            "order_id": "O002",
            "mamamboga": self.mamamboga.id,
            "product": self.product.product_id,
            "community": self.community.community_id,
            "quantity": 5,
            "total_price": "2000.00",
            "deadline_at": timezone.now().isoformat(),
            "order_date": timezone.now().isoformat(),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(response.data['total_price'], "2000.00")

    def test_list_orders(self):
        url = reverse('orders-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list) or 'results' in response.data)

    def test_retrieve_order(self):
        url = reverse('orders-detail', args=[self.order.order_id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_id'], self.order.order_id)

    def test_update_order(self):
        url = reverse('orders-detail', args=[self.order.order_id])
        data = {
            "order_id": self.order.order_id,
            "mamamboga": self.mamamboga.id,
            "product": self.product.product_id,
            "community": self.community.community_id,
            "quantity": 10,
            "total_price": "3000.00",
            "deadline_at": timezone.now().isoformat(),
            "order_date": timezone.now().isoformat(),
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(str(self.order.total_price), "3000.00")

    def test_delete_order(self):
        url = reverse('orders-detail', args=[self.order.order_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(order_id=self.order.order_id).exists())