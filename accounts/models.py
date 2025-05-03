from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    is_approved = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} ({self.specialization})"

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='patient_profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()
