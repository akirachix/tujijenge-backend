from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase # type: ignore
from rest_framework import status # type: ignore
from django.urls import reverse # type: ignore
from communities.models import Community 

class CommunityAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('community-list')  
        self.valid_data = {
            "community_id": "C001",
            "location": "Juja"
        }

    def test_create_community(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_communities(self):
        Community.objects.create(
            community_id="C002",
            location="Kaloleni"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_community(self):
        community = Community.objects.create(
            community_id="C003",
            location="Kaloleni"
        )
        url = reverse('community-detail', args=[community.pk])
        updated_data = {
            "community_id": "C003",
            "location": "Nairobi"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location'], "Nairobi")

        community.refresh_from_db()
        self.assertEqual(community.location, "Nairobi")

    def test_delete_community(self):
        community = Community.objects.create(
            community_id="C004",
            location="Korogocho"
        )
        url = reverse('community-detail', args=[community.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_community_data(self):
        bad_data = {
            "community_id": "",  
            "location": "",  
        }
        response = self.client.post(self.url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



