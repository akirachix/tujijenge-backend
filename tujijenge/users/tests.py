from django.test import TestCase
from users.models import Mamamboga, Stakeholder

class MamambogaModelTests(TestCase):
    def setUp(self):
        self.mamamboga = Mamamboga.objects.create(
            mamamboga_id="M001",
            mamamboga_name="Arsema",
            phone_number="+2579394224",
            pin="1234",
            latitude=10.1,
            longitude=20.2,
            is_active=True
        )

    def test_create_mamamboga(self):
        self.assertEqual(self.mamamboga.mamamboga_id, "M001")
        self.assertEqual(self.mamamboga.mamamboga_name, "Arsema")
        self.assertEqual(self.mamamboga.phone_number, "+2579394224")
        self.assertEqual(self.mamamboga.pin, "1234")
        self.assertTrue(self.mamamboga.is_active)
        self.assertEqual(self.mamamboga.latitude, 10.1)
        self.assertEqual(self.mamamboga.longitude, 20.2)

    def test_default_certified_status(self):
        self.assertEqual(self.mamamboga.certified_status, "Pending")

    def test_str_representation(self):
        self.assertEqual(str(self.mamamboga), "Arsema")

class StakeholderModelTests(TestCase):
    def setUp(self):
        self.stakeholder = Stakeholder.objects.create(
            stakeholder_id="S001",
            stakeholder_name="Taimba",
            stakeholder_email="taimba@gain.com",
            password_hash="hash1"
        )

    def test_create_stakeholder(self):
        self.assertEqual(self.stakeholder.stakeholder_id, "S001")
        self.assertEqual(self.stakeholder.stakeholder_name, "Taimba")
        self.assertEqual(self.stakeholder.stakeholder_email, "taimba@gain.com")
        self.assertEqual(self.stakeholder.password_hash, "hash1")

    def test_str_representation(self):
        self.assertEqual(str(self.stakeholder), "Taimba")