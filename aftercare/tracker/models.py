from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Dr. {self.user.username}"

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


# New models
class VitalSign(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    heart_rate = models.IntegerField()
    blood_pressure = models.CharField(max_length=20)
    oxygen_level = models.IntegerField()
    temperature = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

class RecoveryProgress(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    overall_recovery = models.IntegerField()
    physical_activity = models.IntegerField()
    wound_healing = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()
    purpose = models.TextField()

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
