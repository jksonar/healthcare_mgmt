from django.urls import path
from . import views

urlpatterns = [
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('register/patient/', views.register_patient, name='register_patient'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
