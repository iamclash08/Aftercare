from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    surgery_type = models.CharField(max_length=100)
    surgery_date = models.DateField()
    notes = models.TextField(blank=True)

class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)

class DailyTask(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    medication_taken = models.BooleanField(default=False)
    walked = models.BooleanField(default=False)
    water_intake = models.BooleanField(default=False)

class SymptomLog(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    symptom = models.CharField(max_length=100)
    severity = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    notes = models.TextField(blank=True)
