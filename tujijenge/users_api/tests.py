from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Mamamboga, Stakeholder

class UnifiedUserViewSetTests(APITestCase):
    def setUp(self):
        self.mamamboga = Mamamboga.objects.create(
            first_name="Mamu",
            last_name="Boga",
            phone_number="0712345678",
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
            self.assertIn('phone_number', entry)
            self.assertNotIn('stakeholder_email', entry)

    def test_list_stakeholder(self):
        response = self.client.get('/api/user/?user_type=stakeholder')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for entry in response.data:
            self.assertIn('stakeholder_email', entry)
            self.assertNotIn('phone_number', entry)

    def test_retrieve_mamamboga(self):
        response = self.client.get(f'/api/user/{self.mamamboga.pk}/?user_type=mamamboga')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Mamu")
        self.assertEqual(response.data['phone_number'], "0712345678")

    def test_retrieve_stakeholder(self):
        response = self.client.get(f'/api/user/{self.stakeholder.pk}/?user_type=stakeholder')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Stake")
        self.assertEqual(response.data['stakeholder_email'], "stake@example.com")

    def test_create_mamamboga(self):
        data = {
            "user_type": "mamamboga",
            "first_name": "Alice",
            "last_name": "Wangu",
            "phone_number": "0723456789",
            "pin": "5678"
        }
        response = self.client.post('/api/user/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], "Alice")
        self.assertEqual(response.data['phone_number'], "0723456789")

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

