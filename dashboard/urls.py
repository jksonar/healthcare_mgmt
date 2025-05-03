from django.urls import path
from . import views

urlpatterns = [
    # Main dashboard (role-based)
    path('', views.dashboard, name='dashboard'),

    # Quick access/redirects for each role
    path('appointments/', views.dashboard_appointments, name='dashboard_appointments'),
    path('messages/', views.dashboard_messages, name='dashboard_messages'),
    path('medical-records/', views.dashboard_medical_records, name='dashboard_medical_records'),

    # Doctor-specific: view patients and their records
    path('patients/', views.doctor_patients, name='doctor_patients'),
    path('patients/<int:patient_id>/records/', views.doctor_patient_records, name='doctor_patient_records'),

    # Admin panel shortcut
    path('admin-panel/', views.dashboard_admin_panel, name='dashboard_admin_panel'),
]
