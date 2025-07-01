from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Mamamboga, Stakeholder

class UnifiedUserBasicAPITests(APITestCase):
    def setUp(self):
        self.mamamboga = Mamamboga.objects.create(
            first_name="Jane",
            last_name="Doe",
            phone_number="0712345678",
            pin="1234",
        )
        self.stakeholder = Stakeholder.objects.create(
            first_name="John",
            last_name="Smith",
            stakeholder_email="stake@example.com",
            password_hash="hashedpassword",
        )
        self.list_url = reverse('user-list')

    def test_create_mamamboga(self):
        data = {
            "user_type": "mamamboga",
            "first_name": "New",
            "last_name": "Mamamboga",
            "phone_number": "0798765432",
            "pin": "5678"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_type'], 'mamamboga')

    def test_create_stakeholder(self):
        data = {
            "user_type": "stakeholder",
            "first_name": "New",
            "last_name": "Stakeholder",
            "stakeholder_email": "newstake@example.com",
            "password_hash": "anotherhash"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_type'], 'stakeholder')

    def test_list_all_users(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_mamamboga(self):
        url = reverse('user-detail', args=[self.mamamboga.pk])
        response = self.client.get(url, {'user_type': 'mamamboga'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_type'], 'mamamboga')

    def test_update_mamamboga(self):
        url = reverse('user-detail', args=[self.mamamboga.pk])
        data = {
            "user_type": "mamamboga",
            "first_name": "UpdatedName"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'UpdatedName')

    def test_delete_mamamboga(self):
        url = reverse('user-detail', args=[self.mamamboga.pk])
        response = self.client.delete(url, {'user_type': 'mamamboga'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Mamamboga.objects.filter(pk=self.mamamboga.pk).exists())

    def test_create_mamamboga_missing_fields(self):
        data = {
            "user_type": "mamamboga",
            "first_name": "NoPhone"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)
        self.assertIn('pin', response.data)