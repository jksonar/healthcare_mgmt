from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MedicalRecord, Prescription, MedicalDocument
from .forms import MedicalRecordForm, PrescriptionForm, MedicalDocumentForm
from accounts.models import PatientProfile

# Create your views here.

@login_required
def patient_medical_history(request):
    if hasattr(request.user, 'patientprofile'):
        records = MedicalRecord.objects.filter(patient=request.user.patientprofile)
        return render(request, 'medical/patient_history.html', {'records': records})
    return redirect('login')

@login_required
def doctor_patient_history(request, patient_id):
    if hasattr(request.user, 'doctorprofile'):
        patient = get_object_or_404(PatientProfile, id=patient_id)
        records = MedicalRecord.objects.filter(patient=patient)
        return render(request, 'medical/doctor_patient_history.html', {'records': records, 'patient': patient})
    return redirect('login')

@login_required
def add_medical_record(request, patient_id):
    if not hasattr(request.user, 'doctorprofile'):
        return redirect('login')
    patient = get_object_or_404(PatientProfile, id=patient_id)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.doctor = request.user.doctorprofile
            record.save()
            return redirect('doctor_patient_history', patient_id=patient.id)
    else:
        form = MedicalRecordForm()
    return render(request, 'medical/add_record.html', {'form': form, 'patient': patient})

@login_required
def add_prescription(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    if not hasattr(request.user, 'doctorprofile') or record.doctor != request.user.doctorprofile:
        return redirect('login')
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.record = record
            prescription.save()
            return redirect('doctor_patient_history', patient_id=record.patient.id)
    else:
        form = PrescriptionForm()
    return render(request, 'medical/add_prescription.html', {'form': form, 'record': record})

@login_required
def upload_medical_document(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    if not hasattr(request.user, 'doctorprofile') or record.doctor != request.user.doctorprofile:
        return redirect('login')
    if request.method == 'POST':
        form = MedicalDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.record = record
            doc.save()
            return redirect('doctor_patient_history', patient_id=record.patient.id)
    else:
        form = MedicalDocumentForm()
    return render(request, 'medical/upload_document.html', {'form': form, 'record': record})
