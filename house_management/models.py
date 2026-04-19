from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class House(models.Model):
    PLACE_CHOICE = [
        ('VALLIKAD', 'Vallikad'),
        ('VELLIKULANGARA', 'Vellikulangara'),
    ]
    house_no = models.CharField(max_length=200, unique=True)
    house_name = models.CharField(max_length=200, null=True, blank=True)
    house_owner = models.CharField(max_length=200, null=True, blank=True)
    place = models.CharField(max_length=200, choices=PLACE_CHOICE, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    no_of_members = models.CharField(max_length=200, blank=True, null=True)
    remarks = models.CharField(max_length=100, blank=True, null=True)
    
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.house_no
    

class Member(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        (True, 'Married'),
        (False, 'Single'),
    ]
    
    REMARKS_CHOICES = [
        ('PAT', 'Patients'),
        ('DVC', 'Divorced'),
        ('WID', 'Widow'),
        ('NVR', 'Never Married'),
    ]
    
    EDUCATION_CHOICES = [
        ('PR', 'Primary School'),
        ('HS', 'High School'),
        ('SC', 'Secondary School'),
        ('UG', 'Undergraduate Degree'),
        ('PG', 'Postgraduate Degree'),
        ('PH', 'PhD'),
        ('NT', 'No Formal Education'),
        ('OT', 'Other'),
    ]
    
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    full_name = models.CharField(max_length=400, blank=True, editable=False)
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    education = models.CharField(max_length=2, choices=EDUCATION_CHOICES, blank=True, null=True)
    marital_status = models.BooleanField(choices=MARITAL_STATUS_CHOICES, default=False)
    occupation = models.CharField(max_length=200, null=True, blank=True)
    remarks = models.CharField(max_length=3, choices=REMARKS_CHOICES, null=True, blank=True)
    remarks_description = models.TextField(null=True, blank=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='members')
    
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        
        if self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"
        elif self.first_name:
            self.full_name = self.first_name
        else:
            self.full_name = ""

        # Set added_by based on _user attribute if not already set
        if not self.added_by and hasattr(self, '_user'):
            self.added_by = self._user
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.full_name or "Unnamed Member"
    
    
    
    
    