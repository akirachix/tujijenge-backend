from django.db import models



# Mama Mboga table
from django.db import models

class Mamamboga(models.Model):
    mamamboga_id = models.CharField(max_length=5, primary_key=True)
    mamamboga_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, unique=True)
    pin = models.CharField(max_length=4)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    deactivation_date = models.DateTimeField(null=True, blank=True)
    certified_status = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mamamboga_name

# stakeholders table
class Stakeholder(models.Model):
    stakeholder_id = models.CharField(max_length=5, primary_key=True)
    stakeholder_name = models.CharField(max_length=50)
    stakeholder_email = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stakeholder_name




