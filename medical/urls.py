from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.patient_medical_history, name='patient_medical_history'),
    path('doctor/<int:patient_id>/', views.doctor_patient_history, name='doctor_patient_history'),
    path('doctor/<int:patient_id>/add/', views.add_medical_record, name='add_medical_record'),
    path('record/<int:record_id>/prescription/', views.add_prescription, name='add_prescription'),
    path('record/<int:record_id>/upload/', views.upload_medical_document, name='upload_medical_document'),
]
