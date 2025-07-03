from django.test import TestCase
from django.utils import timezone
from users.models import Mamamboga
from .models import Community, CommunityMembers, TrainingSessions, TrainingRegistration
class CommunityModelsTest(TestCase):
    def setUp(self):
        self.mamamboga = Mamamboga.objects.create(
            phone_number='0712345678',
            first_name='Mama Mwangi',
            last_name='Wanjiku',
        )
        self.community = Community.objects.create(
            name='Community A',
            description='We are here',
            latitude=1.23,
            longitude=36.78,
            created_by=self.mamamboga,
        )
        self.training_session = TrainingSessions.objects.create(
            title='Food Safety',
            description='Training on food safety',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=1),
            is_cancelled=False,
            updated_at=None,
        )
        self.training_registration = TrainingRegistration.objects.create(
            session=self.training_session,
            community=self.community,
            mamamboga=self.mamamboga,
            registration_date=timezone.now()
        )
        self.community_member = CommunityMembers.objects.create(
            mamamboga=self.mamamboga,
            community=self.community,
            joined_date=timezone.now()
        )
    def test_community_creation(self):
        self.assertEqual(self.community.name, 'Community A')
        self.assertEqual(str(self.community), 'Community A')
        self.assertEqual(self.community.created_by, self.mamamboga)
    def test_community_member_creation(self):
        self.assertEqual(self.community_member.mamamboga, self.mamamboga)
        self.assertEqual(self.community_member.community, self.community)
        self.assertIn('in', str(self.community_member))
    def test_training_session_creation(self):
        self.assertEqual(self.training_session.title, 'Food Safety')
        self.assertEqual(str(self.training_session), 'Food Safety')
        self.assertFalse(self.training_session.is_cancelled)
    def test_training_registration(self):
        self.assertEqual(self.training_registration.session, self.training_session)
        self.assertEqual(self.training_registration.community, self.community)
        self.assertEqual(self.training_registration.mamamboga, self.mamamboga)
        self.assertIn('Registration', str(self.training_registration))
    def test_read_community(self):
        community = Community.objects.get(community_id=self.community.community_id)
        self.assertEqual(community.name, 'Community A')
        self.assertEqual(community.description, 'We are here')
    def test_update_community(self):
        self.community.name = 'Greens'
        self.community.save()
        self.assertEqual(self.community.name, 'Greens')
    def test_delete_community(self):
        community_id = self.community.community_id
        Community.objects.get(community_id=community_id).delete()
        with self.assertRaises(Community.DoesNotExist):
            Community.objects.get(community_id=community_id)
    def test_read_training_sessions(self):
        session = TrainingSessions.objects.get(session_id=self.training_session.session_id)
        self.assertEqual(session.title, 'Food Safety')
        self.assertEqual(session.description, 'Training on food safety')
    def test_update_training_session(self):
        self.training_session.title = 'Food Safety 2'
        self.training_session.save()
        self.assertEqual(self.training_session.title, 'Food Safety 2')
    def test_delete_training_sessions(self):
        session_id = self.training_session.session_id
        TrainingSessions.objects.get(session_id=session_id).delete()
        with self.assertRaises(TrainingSessions.DoesNotExist):
            TrainingSessions.objects.get(session_id=session_id)
    def test_read_training_registration(self):
        registration = TrainingRegistration.objects.get(registration_id=self.training_registration.registration_id)
        self.assertEqual(registration.registration_id, self.training_registration.registration_id)
        self.assertEqual(registration.session.title, 'Food Safety')
        self.assertEqual(registration.community.name, 'Community A')
        self.assertEqual(registration.mamamboga.first_name, 'Mama Mwangi')
    def test_update_training_registration(self):
        new_date = timezone.datetime(2022, 1, 1, tzinfo=timezone.get_current_timezone())
        self.training_registration.registration_date = new_date
        self.training_registration.save()
        self.assertEqual(self.training_registration.registration_date, new_date)
    def test_delete_training_registration(self):
        reg_id = self.training_registration.registration_id
        TrainingRegistration.objects.get(registration_id=reg_id).delete()
        with self.assertRaises(TrainingRegistration.DoesNotExist):
            TrainingRegistration.objects.get(registration_id=reg_id)
    def test_read_community_member(self):
        member = CommunityMembers.objects.get(membership_id=self.community_member.membership_id)
        self.assertEqual(member.community, self.community)
    def test_delete_community_member(self):
        member_id = self.community_member.membership_id
        CommunityMembers.objects.get(membership_id=member_id).delete()
        with self.assertRaises(CommunityMembers.DoesNotExist):
            CommunityMembers.objects.get(membership_id=member_id)
