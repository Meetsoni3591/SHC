from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Appointment
from doctors.models import Doctor
from patients.models import Patient
from datetime import datetime, timedelta
from django.utils import timezone

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        queryset = Appointment.objects.all()
        status = self.request.GET.get('status', '')
        date = self.request.GET.get('date', '')
        
        if status:
            queryset = queryset.filter(status=status)
        if date:
            try:
                search_date = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(appointment_date=search_date)
            except ValueError:
                pass
                
        return queryset.order_by('appointment_date', 'appointment_time')

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment_detail.html'
    context_object_name = 'appointment'

@login_required
def create_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        patient_id = request.POST.get('patient')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')
        priority = request.POST.get('priority', 'MEDIUM')

        try:
            doctor = Doctor.objects.get(id=doctor_id)
            patient = Patient.objects.get(id=patient_id)
            
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason,
                priority=priority
            )
            
            messages.success(request, 'Appointment scheduled successfully.')
            return redirect('appointment_detail', pk=appointment.pk)
            
        except (Doctor.DoesNotExist, Patient.DoesNotExist):
            messages.error(request, 'Invalid doctor or patient selected.')
        except Exception as e:
            messages.error(request, str(e))
    
    doctors = Doctor.objects.filter(is_active=True)
    patients = Patient.objects.filter(is_active=True)
    
    return render(request, 'appointments/appointment_form.html', {
        'doctors': doctors,
        'patients': patients
    })

@login_required
def update_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            messages.success(request, 'Appointment status updated successfully.')
        else:
            messages.error(request, 'Invalid status selected.')
    
    return redirect('appointment_detail', pk=pk)

@login_required
def doctor_appointments(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        today = timezone.now().date()
        upcoming_appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__gte=today,
            status='SCHEDULED'
        ).order_by('appointment_date', 'appointment_time')
        
        return render(request, 'appointments/doctor_appointments.html', {
            'appointments': upcoming_appointments
        })
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('home')

@login_required
def patient_appointments(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    
    return render(request, 'appointments/patient_appointments.html', {
        'patient': patient,
        'appointments': appointments
    })
