from django.db import models

class Mamamboga(models.Model):
<<<<<<< HEAD
    id = models.AutoField( primary_key=True)
=======
    id = models.CharField(max_length=5, primary_key=True)


class Mamamboga(models.Model):
    id = models.AutoField(primary_key=True)

>>>>>>> 53a94605c209e0692f80158e963bc1953f1a1473
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
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
        return f"{self.first_name} {self.last_name}"
<<<<<<< HEAD
    
class Stakeholder(models.Model):
    id = models.AutoField( primary_key=True)
=======

class Stakeholder(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    
class Stakeholder(models.Model):

>>>>>>> 53a94605c209e0692f80158e963bc1953f1a1473
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, unique=True, blank=True)
    stakeholder_email = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"