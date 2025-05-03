from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('approve_doctor/<int:doctor_id>/', views.approve_doctor, name='approve_doctor'),
    path('reject_doctor/<int:doctor_id>/', views.reject_doctor, name='reject_doctor'),
    path('patients/', views.manage_patients, name='manage_patients'),
    path('departments/', views.manage_departments, name='manage_departments'),
    path('announcements/', views.manage_announcements, name='manage_announcements'),
]
