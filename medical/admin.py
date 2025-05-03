from django.contrib import admin
from .models import MedicalRecord, Prescription, MedicalDocument

# Register your models here.
admin.site.register(MedicalRecord)
admin.site.register(Prescription)
admin.site.register(MedicalDocument)
