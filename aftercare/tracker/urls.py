from .views import submit_readings
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import custom_login_view
from .views import login_redirect_view, patient_dashboard, doctor_dashboard
from .views import home_view

urlpatterns = [
    path('home/', home_view, name='home'),
    path('', LoginView.as_view(template_name='login.html'), name='login'),  # root URL → login
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('submit-readings/', submit_readings, name='submit_readings'),
    path('register/', views.register_view, name='register'),
    path('create-patient-profile/', views.create_patient_profile, name='create_patient_profile'),
    path('create-doctor-profile/', views.create_doctor_profile, name='create_doctor_profile'),
    path('redirect-after-login/', login_redirect_view, name='login_redirect'),
    path('patient/', patient_dashboard, name='patient_dashboard'),
    path('doctor/', doctor_dashboard, name='doctor_dashboard'),
#     path('checklist/', views.checklist_view, name='checklist_view'),
#     path('symptom-log/', views.symptom_log_view, name='symptom_log_view'),
#     path('vital-sign/', views.vital_sign_view, name='vital_sign'),
#     path('recovery-progress/', views.recovery_progress_view, name='recovery_progress'),
#     path('appointments/', views.appointment_view, name='appointment'),
#     path('messages/', views.message_view, name='message'),
   ]