from django import forms
from .models import Appointment, DoctorAvailability
from accounts.models import DoctorProfile

class AppointmentBookingForm(forms.ModelForm):
    specialization = forms.ChoiceField(choices=[], required=False)
    location = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Appointment
        fields = ['doctor', 'scheduled_time', 'reason']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate specialization choices dynamically
        specializations = DoctorProfile.objects.values_list('specialization', flat=True).distinct()
        self.fields['specialization'].choices = [('', 'All')] + [(s, s) for s in specializations]
        self.fields['doctor'].queryset = DoctorProfile.objects.filter(is_approved=True)

class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ['day_of_week', 'start_time', 'end_time']
        widgets = {
            'day_of_week': forms.Select(choices=[
                ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')
            ])
        }
