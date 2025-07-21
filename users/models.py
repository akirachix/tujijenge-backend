from django.db import models
from django.contrib.auth.models import User


class Mamamboga(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, unique=True)
    pin = models.CharField(max_length=32)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image=models.ImageField(upload_to='mamamboga_image/',blank=True, null=True)
    is_active = models.BooleanField(default=True)
    deactivation_date = models.DateTimeField(null=True, blank=True)
    certified_status = models.CharField(max_length=15, null=True, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Stakeholder(models.Model):
    ROLE_CHOICES=(
        ('Trainer','trainer'),
        ('Supplier','supplier')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='supplier')
    stakeholder_email = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
