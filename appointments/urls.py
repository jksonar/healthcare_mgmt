from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('my/', views.patient_appointments, name='patient_appointments'),
    path('doctor/', views.doctor_appointments, name='doctor_appointments'),
    path('update/<int:appointment_id>/<str:status>/', views.update_appointment_status, name='update_appointment_status'),
    path('availability/', views.manage_availability, name='manage_availability'),
]
