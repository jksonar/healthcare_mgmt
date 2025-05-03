from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from accounts.models import DoctorProfile, PatientProfile
from .models import Department, Announcement
from .forms import DepartmentForm, AnnouncementForm

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    pending_doctors = DoctorProfile.objects.filter(is_approved=False)
    departments = Department.objects.all()
    announcements = Announcement.objects.order_by('-created_at')[:5]
    return render(request, 'admin_panel/dashboard.html', {
        'pending_doctors': pending_doctors,
        'departments': departments,
        'announcements': announcements,
    })

@user_passes_test(is_admin)
def approve_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    doctor.is_approved = True
    doctor.save()
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def reject_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    doctor.user.delete()  # Remove user and profile
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def manage_patients(request):
    patients = PatientProfile.objects.all()
    return render(request, 'admin_panel/manage_patients.html', {'patients': patients})

@user_passes_test(is_admin)
def manage_departments(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_departments')
    else:
        form = DepartmentForm()
    return render(request, 'admin_panel/manage_departments.html', {
        'departments': departments,
        'form': form,
    })

@user_passes_test(is_admin)
def manage_announcements(request):
    announcements = Announcement.objects.all()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_announcements')
    else:
        form = AnnouncementForm()
    return render(request, 'admin_panel/manage_announcements.html', {
        'announcements': announcements,
        'form': form,
    })
