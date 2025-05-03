from django.db import models
from accounts.models import DoctorProfile, PatientProfile

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} with {self.doctor} at {self.scheduled_time}"

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey('accounts.DoctorProfile', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)  # e.g., 'Monday'
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor} - {self.day_of_week} ({self.start_time}-{self.end_time})"
