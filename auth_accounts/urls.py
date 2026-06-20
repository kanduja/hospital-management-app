from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    # Patient
    path(
        'patient_login/',
        views.patient_login,
        name='patient_login'
    ),

    path(
        'create_account/',
        views.create_account,
        name='create_account'
    ),

    path(
        'patient_dashboard/',
        views.patient_dashboard,
        name='patient_dashboard'
    ),

    # Doctor
    path(
        'doctor_login/',
        views.doctor_login,
        name='doctor_login'
    ),

    path(
        'doctor_dashboard/',
        views.doctor_dashboard,
        name='doctor_dashboard'
    ),

    # Receptionist
    path(
        'receptionist_login/',
        views.receptionist_login,
        name='receptionist_login'
    ),

    path(
        'receptionist_dashboard/',
        views.receptionist_dashboard,
        name='receptionist_dashboard'
    ),



    path(
        'forgot_password',
        views.forgot_password,
        name='forgot_password'
    ),

    path('approve/<int:appointment_id>/',
        views.approve_appointment,
        name='approve_appointment'),

    path('reject/<int:appointment_id>/',
         views.reject_appointment,
         name='reject_appointment'),
    
    path('e_billing/',views.e_billing,name='e_billing'),
    
    path('appointment_booking/',views.appointment_booking,name='appointment_booking'),


     path('upload_prescription/',views.upload_prescription,name='upload_prescription'),
     
     path('patient_history/',views.patient_history,name='patient_history'),
     
     path('patient_prescriptions/',views.patient_prescription,name='patient_prescription'),
     path('bill/',views.bill,name='bill'),

]