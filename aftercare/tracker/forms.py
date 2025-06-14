from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, PatientProfile, DoctorProfile, DailyTask, SymptomLog, VitalSign, RecoveryProgress, Appointment, Message

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['surgery_type', 'surgery_date', 'notes']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['specialization']

class DailyTaskForm(forms.ModelForm):
    class Meta:
        model = DailyTask
        fields = ['medication_taken', 'walked', 'water_intake']

class SymptomLogForm(forms.ModelForm):
    class Meta:
        model = SymptomLog
        fields = ['symptom', 'severity', 'notes']


# New forms
class VitalSignForm(forms.ModelForm):
    class Meta:
        model = VitalSign
        fields = ['heart_rate', 'blood_pressure', 'oxygen_level', 'temperature']

class RecoveryProgressForm(forms.ModelForm):
    class Meta:
        model = RecoveryProgress
        fields = ['overall_recovery', 'physical_activity', 'wound_healing']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'purpose']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
