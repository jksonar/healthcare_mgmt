from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import DoctorProfile, PatientProfile
from appointments.models import Appointment
from medical.models import MedicalRecord
from chat.models import Message
from admin_panel.models import Announcement

@login_required
def dashboard(request):
    user = request.user
    context = {}

    if user.is_superuser:
        # Admin dashboard context
        from admin_panel.models import Department
        context['total_doctors'] = DoctorProfile.objects.count()
        context['pending_doctors'] = DoctorProfile.objects.filter(is_approved=False).count()
        context['total_patients'] = PatientProfile.objects.count()
        context['total_appointments'] = Appointment.objects.count()
        context['departments'] = Department.objects.count()
        context['announcements'] = Announcement.objects.order_by('-created_at')[:3]
        return render(request, 'dashboard/admin_dashboard.html', context)

    elif hasattr(user, 'doctorprofile'):
        doctor = user.doctorprofile
        context['upcoming_appointments'] = Appointment.objects.filter(
            doctor=doctor, status__in=['pending', 'approved']
        ).order_by('scheduled_time')[:5]
        context['patients_count'] = Appointment.objects.filter(
            doctor=doctor, status='approved'
        ).values('patient').distinct().count()
        context['unread_messages'] = Message.objects.filter(receiver=user, is_read=False).count()
        context['announcements'] = Announcement.objects.filter(is_active=True).order_by('-created_at')[:3]
        return render(request, 'dashboard/doctor_dashboard.html', context)

    elif hasattr(user, 'patientprofile'):
        patient = user.patientprofile
        context['upcoming_appointments'] = Appointment.objects.filter(
            patient=patient, status__in=['pending', 'approved']
        ).order_by('scheduled_time')[:5]
        context['medical_records'] = MedicalRecord.objects.filter(patient=patient).order_by('-visit_date')[:3]
        context['unread_messages'] = Message.objects.filter(receiver=user, is_read=False).count()
        context['announcements'] = Announcement.objects.filter(is_active=True).order_by('-created_at')[:3]
        return render(request, 'dashboard/patient_dashboard.html', context)

    else:
        return redirect('login')

@login_required
def dashboard_appointments(request):
    user = request.user
    if user.is_superuser:
        return redirect('admin_dashboard')
    elif hasattr(user, 'doctorprofile'):
        return redirect('doctor_appointments')
    elif hasattr(user, 'patientprofile'):
        return redirect('patient_appointments')
    else:
        return redirect('dashboard')

@login_required
def dashboard_messages(request):
    return redirect('chat_list')

@login_required
def dashboard_medical_records(request):
    user = request.user
    if hasattr(user, 'doctorprofile'):
        return redirect('doctor_patients')
    elif hasattr(user, 'patientprofile'):
        return redirect('patient_medical_history')
    else:
        return redirect('dashboard')

@login_required
def doctor_patients(request):
    # List patients for the doctor (implement as needed)
    pass

@login_required
def doctor_patient_records(request, patient_id):
    # Show records for a specific patient (implement as needed)
    pass

@login_required
def dashboard_admin_panel(request):
    return redirect('admin_dashboard')
