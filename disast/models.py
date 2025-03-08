from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    #groups = models.ManyToManyField(Group, related_name='disast_user_set')
    #user_permissions = models.ManyToManyField(Permission, related_name='disast_user_permissions')
    is_agency = models.BooleanField(default=False)
    is_citizen = models.BooleanField(default=False)
    pass

class Disaster(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=50)
    severity = models.CharField(max_length=50)
    date = models.DateField()
    date_reported = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True) 
    created_by = models.ForeignKey('disast.User', on_delete=models.SET_NULL, null=True, related_name="created_disasters")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title

class Agency(models.Model):
    user = models.OneToOneField('disast.User', on_delete=models.CASCADE)
    agency_name = models.CharField(max_length=200)

class Citizen(models.Model):
    user = models.OneToOneField('disast.User', on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=100)

class FundRequest(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_by = models.ForeignKey('disast.User', on_delete=models.CASCADE, related_name="fund_requests")
    created_at = models.DateTimeField(auto_now_add=True)

class CommunityPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey('disast.User', on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)


