from django.db import models
from django.contrib.auth.models import AbstractUser



# USER MODEL
class User(AbstractUser):

    ROLE_CHOICES = [

        ('patient', 'Patient'),

        ('doctor', 'Doctor'),

        ('receptionist', 'Receptionist'),

        ('admin', 'Admin')

    ]


    role = models.CharField(

        max_length=20,

        choices=ROLE_CHOICES

    )


    phone = models.CharField(

        max_length=15,

        blank=True

    )


    age = models.IntegerField(

        null=True,

        blank=True

    )


    gender = models.CharField(

        max_length=20,

        blank=True

    )


    specialization = models.CharField(

        max_length=100,

        blank=True
    )


    def __str__(self):

        return self.username




# APPOINTMENT

from django.db import models
from .models import User


class Appointment(models.Model):

    STATUS = [

        ("Pending", "Pending"),

        ("Approved", "Approved"),

        ("Rejected", "Rejected")

    ]

    patient = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="patient_appointments"

    )

    doctor = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="doctor_appointments"

    )

    appointment_date = models.DateField(
        null=True,
        blank=True
    )

    appointment_time = models.TimeField(
        null=True,
        blank=True
    )

    symptoms = models.TextField()

    status = models.CharField(

        max_length=20,

        choices=STATUS,

        default="Pending"

    )

    def __str__(self):

        return (

            self.patient.username

            + " → " +

            self.doctor.username

        )



# BILLING
from django.db import models
from .models import User


class Bill(models.Model):

    patient = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    receptionist = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="created_bills"

    )

    consultation_fee = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    medicine_fee = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    tax = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    total_amount = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    payment_time = models.DateTimeField(

        auto_now_add=True

    )

    payment_status = models.CharField(

        max_length=20,

        default="Paid"

    )

    def __str__(self):

        return (

            self.patient.username

        )




# PRESCRIPTION
from django.db import models


class Prescription(models.Model):

    appointment = models.OneToOneField(

        Appointment,

        on_delete=models.CASCADE

    )

    prescription_file = models.FileField(

        upload_to="patient_prescriptions/"

    )

    uploaded_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return (

            self.appointment.patient.username

        )

