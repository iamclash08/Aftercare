from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

@login_required
def login_redirect_view(request):
    user = request.user

    if hasattr(user, 'doctorprofile'):
        return redirect('doctor_dashboard')
    elif hasattr(user, 'patientprofile'):
        return redirect('patient_dashboard')
    else:
        return redirect('default_dashboard')  # Optional fallback

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirect based on role
            if hasattr(user, 'patientprofile'):
                return redirect('patient_dashboard')
            elif hasattr(user, 'doctorprofile'):
                return redirect('doctor_dashboard')
            else:
                return redirect('login')  # fallback
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def home_view(request):
    return render(request, 'home.html')

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on role
            if hasattr(user, 'patientprofile'):
                return redirect('patient_dashboard')
            elif hasattr(user, 'doctorprofile'):
                return redirect('doctor_dashboard')
            else:
                return redirect('login')  # fallback if no role
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form}) 

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

@login_required
def vital_sign_view(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    if request.method == 'POST':
        form = VitalSignForm(request.POST)
        if form.is_valid():
            vital = form.save(commit=False)
            vital.patient = patient
            vital.save()
            return redirect('patient_dashboard')
    else:
        form = VitalSignForm()
    return render(request, 'tracker/vital_sign.html', {'form': form})

@login_required
def recovery_progress_view(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    if request.method == 'POST':
        form = RecoveryProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.patient = patient
            progress.save()
            return redirect('patient_dashboard')
    else:
        form = RecoveryProgressForm()
    return render(request, 'tracker/recovery_progress.html', {'form': form})

@login_required
def appointment_view(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'tracker/appointment.html', {'form': form})

@login_required
def message_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('patient_dashboard')
    else:
        form = MessageForm()
    return render(request, 'tracker/message.html', {'form': form})


from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from io import BytesIO

def submit_readings(request):
    if request.method == 'POST':
        data = {
            'bp': request.POST.get('bp'),
            'temp': request.POST.get('temp'),
            'oxy': request.POST.get('oxy'),
            'heart': request.POST.get('heart'),
            'symptoms': request.POST.get('symptoms'),
            'checklist': request.POST.getlist('checklist')
        }

        # Generate PDF
        template = get_template('tracker/pdf_template.html')
        html = template.render(data)
        buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=buffer)

        if not pisa_status.err:
            # Email PDF
            pdf = buffer.getvalue()
            email = EmailMessage(
                'Patient Daily Report',
                'Please find attached daily report.',
                'from@example.com',
                ['doctor@example.com'],
            )
            email.attach('daily_report.pdf', pdf, 'application/pdf')
            email.send()
            return HttpResponse("Report sent successfully.")
        else:
            return HttpResponse("PDF generation error.")
    return HttpResponse("Invalid request")
