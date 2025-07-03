from django.test import TestCase
from users.models import Mamamboga, Stakeholder

class MamambogaModelTests(TestCase):
    def setUp(self):
        self.mamamboga = Mamamboga.objects.create(
            first_name="Test",
            last_name="User",
            phone_number="0700000000",
            pin="1234"
        )

    def test_create_mamamboga(self):
        self.assertEqual(self.mamamboga.first_name, "Test")
        self.assertEqual(self.mamamboga.last_name, "User")
        self.assertEqual(self.mamamboga.phone_number, "0700000000")
        self.assertEqual(self.mamamboga.pin, "1234")

    def test_str_representation(self):
        self.assertEqual(str(self.mamamboga), "Test User")

    def test_default_certified_status(self):
        self.assertIsNone(self.mamamboga.certified_status)

class StakeholderModelTests(TestCase):
    def setUp(self):
        self.stakeholder = Stakeholder.objects.create(
            first_name="Stake",
            last_name="Holder",
            stakeholder_email="stake@example.com",
            password_hash="secret"
        )

    def test_create_stakeholder(self):
        self.assertEqual(self.stakeholder.first_name, "Stake")
        self.assertEqual(self.stakeholder.last_name, "Holder")
        self.assertEqual(self.stakeholder.stakeholder_email, "stake@example.com")
        self.assertEqual(self.stakeholder.password_hash, "secret")

    def test_str_representation(self):
        self.assertEqual(str(self.stakeholder), "Stake Holder")