from django.urls import path
from . import views
from tracker.views import home_view

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('create-patient-profile/', views.create_patient_profile, name='create_patient_profile'),
    path('create-doctor-profile/', views.create_doctor_profile, name='create_doctor_profile'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('checklist/', views.checklist_view, name='checklist_view'),
    path('symptom-log/', views.symptom_log_view, name='symptom_log_view'),
    path('', home_view, name='home'),
]
