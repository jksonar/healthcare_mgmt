from django.db import models
from accounts.models import PatientProfile, DoctorProfile

# Create your models here.

class MedicalRecord(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    treatment = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient} - {self.visit_date.date()}"

class Prescription(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medication} for {self.record.patient}"

class MedicalDocument(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='medical_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Document for {self.record.patient} ({self.uploaded_at.date()})"

class Feedback(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.patient} for {self.doctor}"
