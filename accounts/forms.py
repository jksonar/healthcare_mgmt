from django import forms
from django.contrib.auth.models import User
from .models import DoctorProfile, PatientProfile

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

class DoctorRegisterForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'department', 'phone', 'bio', 'profile_pic']

class PatientRegisterForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'phone', 'address', 'profile_pic']
