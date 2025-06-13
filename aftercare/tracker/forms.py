from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, PatientProfile, DoctorProfile, DailyTask, SymptomLog

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
