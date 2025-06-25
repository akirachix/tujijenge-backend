# from django.test import TestCase

# # Create your tests here.
# from rest_framework.test import APITestCase # type: ignore
# from rest_framework import status # type: ignore
# from django.urls import reverse # type: ignore
# from communities.models import Community 

# class CommunityAPITest(APITestCase):
#     def setUp(self):
#         self.url = reverse('community-list')  
#         self.valid_data = {
#             "community_id": "C001",
#             "location": "Juja"
#         }

#     def test_create_community(self):
#         response = self.client.post(self.url, self.valid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_list_communities(self):
#         Community.objects.create(
#             community_id="C002",
#             location="Kaloleni"
#         )
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertGreaterEqual(len(response.data), 1)

#     def test_update_community(self):
#         community = Community.objects.create(
#             community_id="C003",
#             location="Kaloleni"
#         )
#         url = reverse('community-detail', args=[community.pk])
#         updated_data = {
#             "community_id": "C003",
#             "location": "Nairobi"
#         }
#         response = self.client.put(url, updated_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['location'], "Nairobi")

#         community.refresh_from_db()
#         self.assertEqual(community.location, "Nairobi")

#     def test_delete_community(self):
#         community = Community.objects.create(
#             community_id="C004",
#             location="Korogocho"
#         )
#         url = reverse('community-detail', args=[community.pk])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_invalid_community_data(self):
#         bad_data = {
#             "community_id": "",  
#             "location": "",  
#         }
#         response = self.client.post(self.url, bad_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



from django.test import TestCase
from django.utils import timezone
from users.models import Mamamboga  # Adjust import as needed
from .models import Community, CommunityMembers, TrainingSessions, TrainingRegistration

class ModelTests(TestCase):
    def setUp(self):
        # Create a Mamamboga user
        self.mamamboga = Mamamboga.objects.create(
            mamamboga_id='M001',  # adjust field names as per your Mamamboga model
            mamamboga_name='Mama Jane'
        )

        self.community = Community.objects.create(
            community_id='C001',
            name='Test Community',
            description='A test community',
            latitude=-1.2921,
            longitude=36.8219,
            created_by=self.mamamboga
        )

        self.training_session = TrainingSessions.objects.create(
            session_id='TS001',
            title='Food Safety',
            description='Training on food safety',
            start_date=timezone.now(),
            end_date=None,
            is_cancelled=False,
            updated_at=None
        )

    def test_community_creation(self):
        self.assertEqual(self.community.name, 'Test Community')
        self.assertEqual(str(self.community), 'Test Community')
        self.assertEqual(self.community.created_by, self.mamamboga)

    def test_community_member_creation(self):
        member = CommunityMembers.objects.create(
            membership_id='CM001',
            mamamboga=self.mamamboga,
            community=self.community,
            joined_date=timezone.now()
        )
        self.assertEqual(member.mamamboga, self.mamamboga)
        self.assertEqual(member.community, self.community)
        self.assertIn('in', str(member))

    def test_trainingsession_creation(self):
        self.assertEqual(self.training_session.title, 'Food Safety')
        self.assertEqual(str(self.training_session), 'Food Safety')
        self.assertFalse(self.training_session.is_cancelled)

    def test_training_registration(self):
        registration = TrainingRegistration.objects.create(
            registration_id='R001',
            session=self.training_session,
            community=self.community,
            mamamboga=self.mamamboga,
            registration_date=timezone.now()
        )
        self.assertEqual(registration.session, self.training_session)
        self.assertEqual(registration.community, self.community)
        self.assertEqual(registration.mamamboga, self.mamamboga)
        self.assertIn('Registration', str(registration))

    def test_nullable_fields(self):
        # Test that nullable fields can be left blank
        community = Community.objects.create(
            community_id='C002',
            name='Null Community',
            created_by=self.mamamboga
        )
        self.assertIsNone(community.description)
        self.assertIsNone(community.latitude)
        self.assertIsNone(community.longitude)

        session = TrainingSessions.objects.create(
            session_id='TS002',
            title='Null Session'
        )
        self.assertIsNone(session.description)
        self.assertIsNone(session.start_date)
        self.assertIsNone(session.end_date)
        self.assertIsNone(session.updated_at)

        registration = TrainingRegistration.objects.create(
            registration_id='R002',
            session=session,
            community=community,
            mamamboga=self.mamamboga
        )
        self.assertIsNone(registration.registration_date)
        self.assertIsNone(registration.cancelled_at)