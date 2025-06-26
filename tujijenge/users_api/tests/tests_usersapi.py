from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import Mamamboga, Stakeholder

class UserPolymorphicAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse('users-crud-list')
        self.mamamboga = Mamamboga.objects.create(
            mamamboga_id="M001",
            mamamboga_name="Arsema",
            phone_number="+2579394224",
            pin="1234",
            latitude=10.1,
            longitude=20.2,
            is_active=True,
            certified_status="Pending"
        )
        self.stakeholder = Stakeholder.objects.create(
            stakeholder_id="S001",
            stakeholder_name="Taimba",
            stakeholder_email="taimba@gain.com",
            password_hash="hash1"
        )
        self.mamamboga_detail_url = reverse('users-crud-detail', args=[self.mamamboga.mamamboga_id])
        self.stakeholder_detail_url = reverse('users-crud-detail', args=[self.stakeholder.stakeholder_id])

    def test_list_users(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_create_mamamboga(self):
        data = {
            "user_type": "mamamboga",
            "mamamboga_id": "M002",
            "mamamboga_name": "Meron",
            "phone_number": "+238720943",
            "pin": "4321",
            "latitude": 3.3,
            "longitude": 4.4,
            "is_active": True,
            "certified_status": "Pending"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mamamboga.objects.count(), 2)

    def test_create_stakeholder(self):
        data = {
            "user_type": "stakeholder",
            "stakeholder_id": "S002",
            "stakeholder_name": "Gain",
            "stakeholder_email": "gain@gain.com",
            "password_hash": "hash2"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Stakeholder.objects.count(), 2)

    def test_create_invalid_stakeholder(self):
        data = {
            "user_type": "stakeholder",
            "stakeholder_id": "S003",
            "stakeholder_name": "",
            "stakeholder_email": "",
            "password_hash": ""
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_mamamboga(self):
        response = self.client.get(self.mamamboga_detail_url + '?user_type=mamamboga')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mamamboga_name'], "Arsema")

    def test_retrieve_stakeholder(self):
        response = self.client.get(self.stakeholder_detail_url + '?user_type=stakeholder')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stakeholder_name'], "Taimba")

    def test_update_mamamboga(self):
        data = {
            "user_type": "mamamboga",
            "mamamboga_id": "M001",
            "mamamboga_name": "Saloi",
            "phone_number": "0700000001",
            "pin": "1234",
            "latitude": 1.1,
            "longitude": 2.2,
            "is_active": False,
            "certified_status": "Pending"
        }
        response = self.client.put(self.mamamboga_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Mamamboga.objects.get(pk="M001").mamamboga_name, "Saloi")

    def test_update_stakeholder(self):
        data = {
            "user_type": "stakeholder",
            "stakeholder_id": "S001",
            "stakeholder_name": "GainUpdated",
            "stakeholder_email": "gainupdated@gain.com",
            "password_hash": "hash1"
        }
        response = self.client.put(self.stakeholder_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Stakeholder.objects.get(pk="S001").stakeholder_name, "GainUpdated")

    def test_delete_mamamboga(self):
        response = self.client.delete(self.mamamboga_detail_url + '?user_type=mamamboga')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Mamamboga.objects.filter(pk="M001").exists())

    def test_delete_stakeholder(self):
        response = self.client.delete(self.stakeholder_detail_url + '?user_type=stakeholder')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Stakeholder.objects.filter(pk="S001").exists())