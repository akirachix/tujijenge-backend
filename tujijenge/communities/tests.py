


from django.test import TestCase
from django.db.utils import IntegrityError
from datetime import timedelta
from django.utils import timezone
from users.models import Mamamboga  
from .models import Community, CommunityMembers, TrainingSessions, TrainingRegistration

class ModelTests(TestCase):
    def setUp(self):
        self.mamamboga = Mamamboga.objects.create(
            id='M001',  
            first_name='Mama Mwangi'
        )

        self.community = Community.objects.create(
            community_id='C001',
            name='Community A',
            description='We are here',
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

        self.training_registration = TrainingRegistration.objects.create(
            registration_id='R001',
            session=self.training_session,
            community=self.community,
            mamamboga=self.mamamboga,
            registration_date=timezone.now()
        )
        self.community_member = CommunityMembers.objects.create(
            membership_id='CM001',
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

        self.assertEqual(self.training_registration.session, self.training_session)
        self.assertEqual(self.training_registration.community, self.community)
        self.assertEqual(self.training_registration.mamamboga, self.mamamboga)

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
        
    def test_read_community(self):
        community = Community.objects.get(community_id ='C001')
        self.assertEqual(community.name, 'Community A')
        self.assertEqual(community.description, 'We are here')
        
    def test_update_community(self):
        self.community.name = 'Greens'
        self.community.save()
        self.assertEqual(self.community.name, 'Greens')
        
    def test_delete_community(self):
         community = Community.objects.get(community_id ='C001')
         community.delete()
         with self.assertRaises(Community.DoesNotExist):
             Community.objects.get(community_id ='C001')
    
    def test_read_training_sessions(self):
        session = TrainingSessions.objects.get(session_id='TS001')
        self.assertEqual(session.title, 'Food Safety')
        self.assertEqual(session.description, 'Training on food safety')
        
    def test_update_training_session(self):
        self.training_session.title = 'Food Safety 2'
        self.training_session.save()
        self.assertEqual(self.training_session.title, 'Food Safety 2')
    
    def test_delete_training_sessions(self):
        session = TrainingSessions.objects.get(session_id='TS001')
        session.delete()
        with self.assertRaises(TrainingSessions.DoesNotExist):
            TrainingSessions.objects.get(session_id='TS001')
            
              
    def test_read_training_registrations(self):
        registration = TrainingRegistration.objects.get(registration_id='R001')
        self.assertEqual(registration.registration_id, 'R001')
        self.assertEqual(registration.session.title, 'Food Safety')
        self.assertEqual(registration.community.name, 'Community A')
        self.assertEqual(registration.mamamboga.first_name, 'Mama Mwangi')
        
    def test_update_training_registrations(self):
        self.training_registration.registration_date = '2022-01-01'
        self.training_registration.save()
        self.assertEqual(self.training_registration.registration_date, '2022-01-01')
        
    def test_delete_training_registrations(self):
        registration = TrainingRegistration.objects.get(registration_id='R001')
        registration.delete()
        with self.assertRaises(TrainingRegistration.DoesNotExist):
            TrainingRegistration.objects.get(registration_id='R001')
        
    
    def test_read_community_member(self):
        member = CommunityMembers.objects.get(
            membership_id='CM001',
        )
        self.assertEqual(member.community, self.community)
        
    def test_delete_community_member(self):
        member = CommunityMembers.objects.get(
            membership_id='CM001',
        )
        member.delete()
        with self.assertRaises(CommunityMembers.DoesNotExist):
            CommunityMembers.objects.get(
                membership_id='CM001',
            )
        
            
        
 
