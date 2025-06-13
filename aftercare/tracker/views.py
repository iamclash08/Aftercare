from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'patient':
                return redirect('create_patient_profile')
            else:
                return redirect('create_doctor_profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def create_patient_profile(request):
    if request.user.role != 'patient':
        return redirect('doctor_dashboard')
    if request.method == 'POST':
        form = PatientProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('patient_dashboard')
    else:
        form = PatientProfileForm()
    return render(request, 'tracker/patient_profile.html', {'form': form})

@login_required
def create_doctor_profile(request):
    if request.user.role != 'doctor':
        return redirect('patient_dashboard')
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('doctor_dashboard')
    else:
        form = DoctorProfileForm()
    return render(request, 'tracker/doctor_profile.html', {'form': form})

@login_required
def patient_dashboard(request):
    profile = get_object_or_404(PatientProfile, user=request.user)
    tasks = DailyTask.objects.filter(patient=profile).order_by('-date')
    symptoms = SymptomLog.objects.filter(patient=profile).order_by('-date')
    return render(request, 'tracker/patient_dashboard.html', {
        'profile': profile,
        'tasks': tasks,
        'symptoms': symptoms,
    })

@login_required
def doctor_dashboard(request):
    profile = get_object_or_404(DoctorProfile, user=request.user)
    patients = PatientProfile.objects.all()
    return render(request, 'tracker/doctor_dashboard.html', {
        'profile': profile,
        'patients': patients,
    })

@login_required
def checklist_view(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    if request.method == 'POST':
        form = DailyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.patient = patient
            task.save()
            return redirect('patient_dashboard')
    else:
        form = DailyTaskForm()
    return render(request, 'tracker/checklist.html', {'form': form})

@login_required
def symptom_log_view(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    if request.method == 'POST':
        form = SymptomLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.patient = patient
            log.save()
            return redirect('patient_dashboard')
    else:
        form = SymptomLogForm()
    return render(request, 'tracker/symptom_log.html', {'form': form})
