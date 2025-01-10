from django.shortcuts import render
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

def home(request):
    context = {
        'doctor_count': Doctor.objects.count(),
        'patient_count': Patient.objects.count(),
        'appointment_count': Appointment.objects.filter(status='COMPLETED').count(),
    }
    return render(request, 'main.html', context)
