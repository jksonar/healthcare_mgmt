from django.shortcuts import render, redirect
from .forms import AppointmentBookingForm, DoctorAvailabilityForm
from .models import Appointment, DoctorAvailability
from accounts.models import DoctorProfile, PatientProfile
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def book_appointment(request):
    if not hasattr(request.user, 'patientprofile'):
        return redirect('login')

    doctors = DoctorProfile.objects.filter(is_approved=True)
    specialization = request.GET.get('specialization', '')
    location = request.GET.get('location', '')

    if specialization:
        doctors = doctors.filter(specialization=specialization)
    if location:
        doctors = doctors.filter(location__icontains=location)

    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        form.fields['doctor'].queryset = doctors
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patientprofile
            appointment.status = 'pending'
            appointment.save()
            return redirect('patient_appointments')
    else:
        form = AppointmentBookingForm()
        form.fields['doctor'].queryset = doctors

    # For filter dropdowns
    specializations = DoctorProfile.objects.values_list('specialization', flat=True).distinct()
    locations = DoctorProfile.objects.values_list('location', flat=True).distinct()

    return render(request, 'appointments/book_appointment.html', {
        'form': form,
        'specializations': specializations,
        'locations': locations,
        'selected_specialization': specialization,
        'selected_location': location,
    })

@login_required
def patient_appointments(request):
    if hasattr(request.user, 'patientprofile'):
        appointments = Appointment.objects.filter(patient=request.user.patientprofile)
        return render(request, 'appointments/patient_appointments.html', {'appointments': appointments})
    else:
        return redirect('login')

@login_required
def doctor_appointments(request):
    if hasattr(request.user, 'doctorprofile'):
        appointments = Appointment.objects.filter(doctor=request.user.doctorprofile)
        return render(request, 'appointments/doctor_appointments.html', {'appointments': appointments})
    else:
        return redirect('login')

@login_required
def update_appointment_status(request, appointment_id, status):
    if hasattr(request.user, 'doctorprofile'):
        appointment = Appointment.objects.get(id=appointment_id, doctor=request.user.doctorprofile)
        if status in ['approved', 'rejected', 'completed', 'cancelled']:
            appointment.status = status
            appointment.save()
        return redirect('doctor_appointments')
    else:
        return redirect('login')

@login_required
def manage_availability(request):
    if not hasattr(request.user, 'doctorprofile'):
        return redirect('login')
    doctor = request.user.doctorprofile
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor = doctor
            availability.save()
            return redirect('manage_availability')
    else:
        form = DoctorAvailabilityForm()
    availabilities = DoctorAvailability.objects.filter(doctor=doctor)
    return render(request, 'appointments/manage_availability.html', {
        'form': form,
        'availabilities': availabilities
    })
