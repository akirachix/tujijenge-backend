from django.db import models


class Community(models.Model):
   
   community_id = models.CharField(max_length=5, primary_key=True)
   name = models.CharField(max_length=255)
   description = models.TextField(null=True, blank=True)
   latitude = models.FloatField(null=True, blank=True)
   longitude = models.FloatField(null=True, blank=True)
   created_by = models.ForeignKey(
       "users.Mamamboga",
       on_delete=models.CASCADE,
       related_name='communities_created'
   )

   def __str__(self):
       return self.name


class CommunityMembers(models.Model):
  
   membership_id = models.CharField(max_length=5, primary_key=True)
   mamamboga = models.ForeignKey(
       "users.Mamamboga",
       on_delete=models.CASCADE,
       related_name='community_memberships'
   )
   community = models.ForeignKey(
       Community,
       on_delete=models.CASCADE,
       related_name='members'
   )
   joined_date = models.DateTimeField(null=True, blank=True)
   left_date = models.DateTimeField(null=True, blank=True)


   def __str__(self):
       return f"{self.mamamboga.mamamboga_name} in {self.community.name}"


class TrainingSessions(models.Model):
 
   session_id = models.CharField(max_length=5, primary_key=True)
   title = models.CharField(max_length=255)
   description = models.TextField(null=True, blank=True)
   start_date = models.DateTimeField(null=True, blank=True)
   end_date = models.DateTimeField(null=True, blank=True)
   is_cancelled = models.BooleanField(default=False)
   updated_at = models.DateTimeField(null=True, blank=True)


   def __str__(self):
       return self.title


class TrainingRegistration(models.Model):
   """Represents a vendor's registration for a training session."""
   registration_id = models.CharField(max_length=5, primary_key=True)
   session = models.ForeignKey(
       TrainingSessions,
       on_delete=models.CASCADE,
       related_name='registrations'
   )
   community = models.ForeignKey(
       Community,
       on_delete=models.CASCADE,
       related_name='training_registrations'
   )
   mamamboga = models.ForeignKey(
       "users.Mamamboga",
       on_delete=models.CASCADE,
       related_name='training_registrations'
   )
   registration_date = models.DateTimeField(null=True, blank=True)
   cancelled_at = models.DateTimeField(null=True, blank=True)



   def __str__(self):
       return f"Registration {self.registration_id} for {self.session.title}"
