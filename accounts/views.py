from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, DoctorRegisterForm, PatientRegisterForm
from .models import DoctorProfile, PatientProfile
from django.contrib.auth.models import User

# Create your views here.

def register_doctor(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = DoctorRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Doctor registered! Await admin approval.')
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = DoctorRegisterForm()
    return render(request, 'accounts/register_doctor.html', {'user_form': user_form, 'profile_form': profile_form})

def register_patient(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = PatientRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Patient registered! You can now log in.')
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = PatientRegisterForm()
    return render(request, 'accounts/register_patient.html', {'user_form': user_form, 'profile_form': profile_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')
