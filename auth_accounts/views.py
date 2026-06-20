
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User, Appointment, Bill
from .models import Bill, User
from django.contrib.auth.hashers import make_password
from .models import User


# HOME
def home(request):
    return render(request, "home.html")


# ================= LOGIN =================

def patient_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.role == "patient":

            login(request, user)

            return redirect(
                "patient_dashboard"
            )

        return render(
            request,
            "patient_login.html",
            {
                "error":
                "Invalid patient credentials"
            }
        )

    return render(
        request,
        "patient_login.html"
    )



def doctor_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        print(
            "USERNAME =",
            username
        )

        user = authenticate(

            request,

            username=username,

            password=password

        )

        print(
            "USER =",
            user
        )

        if user is not None:

            print(
                "ROLE =",
                user.role
            )

            if user.role == "doctor":

                login(

                    request,

                    user

                )

                print(
                    "LOGIN SUCCESS"
                )

                return redirect(

                    "doctor_dashboard"

                )

        print(
            "LOGIN FAILED"
        )

        return render(

            request,

            "doctor_login.html",

            {

                "error":

                "Wrong username or password"

            }

        )

    return render(

        request,

        "doctor_login.html"

    )


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def receptionist_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        print(
            "USERNAME:",
            username
        )

        user = authenticate(

            request,

            username=username,

            password=password

        )

        print(
            "USER:",
            user
        )

        if user is not None:

            print(
                "ROLE:",
                user.role
            )

            if user.role.lower() == "receptionist":

                login(

                    request,

                    user

                )

                print(
                    "LOGIN SUCCESS"
                )

                return redirect(

                    "receptionist_dashboard"

                )

        print(
            "LOGIN FAILED"
        )

        return render(

            request,

            "receptionist_login.html",

            {

                "error":

                "Invalid receptionist credentials"

            }

        )

    return render(

        request,

        "receptionist_login.html"

    )

def forgot_password(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        try:

            user = User.objects.get(

                username=username

            )

            user.password = make_password(

                password

            )

            user.save()

            return redirect(

                "home"

            )

        except:

            pass


    return render(

        request,

        "forgot_password.html"

    )


# ================= REGISTER =================

def create_account(request):

    if request.method == "POST":

        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        age = request.POST.get("age")
        gender = request.POST.get("gender")

        password = request.POST.get("password")
        confirm = request.POST.get(
            "confirm_password"
        )

        if password != confirm:

            return render(
                request,
                "create_account.html",
                {
                    "error":
                    "Passwords do not match"
                }
            )

        if User.objects.filter(
            email=email
        ).exists():

            return render(
                request,
                "create_account.html",
                {
                    "error":
                    "Email already registered"
                }
            )

        user = User.objects.create_user(
            username=fullname,
            email=email,
            password=password
        )

        user.phone = phone
        user.age = age
        user.gender = gender
        user.role = "patient"

        user.save()

        return redirect(
            "patient_login"
        )

    return render(
        request,
        "create_account.html"
    )


# ================= DASHBOARDS =================

def patient_dashboard(request):

    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by(
        "-appointment_date",
        "-appointment_time"
    )

    return render(

        request,

        "patient_dashboard.html",

        {

            "appointments":
            appointments

        }

    )


def doctor_dashboard(request):

    appointments = Appointment.objects.filter(
        doctor=request.user
    )

    return render(
        request,
        "doctor_dashboard.html",
        {
            "appointments":
            appointments
        }
    )


from django.shortcuts import render
from .models import Appointment


def receptionist_dashboard(request):

    appointments = Appointment.objects.all().order_by(

        "-appointment_date",

        "-appointment_time"

    )
    return render(
        request,
        "receptionist_dashboard.html",
        {
            "appointments": appointments
            }
        )


# ================= APPOINTMENT =================

def appointment_booking(request):

    doctors = User.objects.filter(
        role="doctor"
    )

    if request.method == "POST":

        doctor_id = request.POST.get(
            "doctor"
        )

        doctor = User.objects.get(
            id=doctor_id
        )

        Appointment.objects.create(

            patient=request.user,

            doctor=doctor,

            appointment_date=request.POST.get(
                "appointment_date"
            ),

            appointment_time=request.POST.get(
                "appointment_time"
            ),

            symptoms=request.POST.get(
                "symptoms"
            ),

            status="Pending"
        )

        return redirect(
            "patient_dashboard"
        )

    return render(
        request,
        "appointment_booking.html",
        {
            "doctors":
            doctors
        }
    )


# ================= APPROVAL =================

def approve_appointment(
    request,
    appointment_id
):

    appointment = Appointment.objects.get(
        id=appointment_id
    )

    appointment.status = "Approved"

    appointment.save()

    return redirect(
        "doctor_dashboard"
    )


def reject_appointment(
    request,
    appointment_id
):

    appointment = Appointment.objects.get(
        id=appointment_id
    )

    appointment.status = "Rejected"

    appointment.save()

    return redirect(
        "doctor_dashboard"
    )


# ================= BILLING =================

from django.shortcuts import render
from .models import Bill


def e_billing(request):

    bills = Bill.objects.filter(

        patient=request.user

    )

    return render(

        request,

        "e_billing.html",

        {

            "bills":

            bills

        }

    )


# ================= PRESCRIPTION =================
from django.shortcuts import render, redirect
from .models import Appointment, Prescription


def upload_prescription(request):

    appointments = Appointment.objects.filter(

        doctor=request.user,

        status="Approved"

    )

    if request.method == "POST":

        appointment_id = request.POST.get(

            "appointment"

        )

        file = request.FILES.get(

            "prescription"

        )

        appointment = Appointment.objects.get(

            id=appointment_id

        )

        Prescription.objects.update_or_create(

            appointment=appointment,

            defaults={

                "prescription_file": file

            }

        )

        return redirect(

            "doctor_dashboard"

        )

    return render(

        request,

        "upload_prescription.html",

        {

            "appointments":

            appointments

        }

    )


def patient_history(request):

    appointments = Appointment.objects.filter(

        patient=request.user

    )


    return render(

        request,

        "patient_history.html",

        {

            "appointments":

            appointments

        }

    )

from django.shortcuts import render
from .models import Prescription


def patient_prescription(request):

    prescriptions = Prescription.objects.filter(

        appointment__patient=request.user

    )

    return render(

        request,

        "patient_prescription.html",

        {

            "prescriptions":

            prescriptions

        }

    )
def bill(request):

    patients = User.objects.filter(
        role="patient"
    )

    if request.method == "POST":

        patient = User.objects.get(
            id=request.POST.get(
                "patient"
            )
        )

        consultation = float(
            request.POST.get(
                "consultation"
            )
        )

        medicine = float(
            request.POST.get(
                "medicine"
            )
        )

        tax = float(
            request.POST.get(
                "tax"
            )
        )

        total = (
            consultation
            +
            medicine
            +
            tax
        )

        Bill.objects.create(

            patient=patient,

            receptionist=request.user,

            consultation_fee=consultation,

            medicine_fee=medicine,

            tax=tax,

            total_amount=total

        )

        return redirect(
            "receptionist_dashboard"
        )


    return render(

        request,

        "bill.html",

        {

            "patients": patients

        }

    )