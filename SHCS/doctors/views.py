from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Doctor
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'doctors/doctor_list.html'
    context_object_name = 'doctors'
    paginate_by = 10

    def get_queryset(self):
        queryset = Doctor.objects.filter(is_active=True)
        specialization = self.request.GET.get('specialization', '')
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        return queryset

class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor
    template_name = 'doctors/doctor_detail.html'
    context_object_name = 'doctor'

@login_required
def doctor_profile(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        return render(request, 'doctors/doctor_profile.html', {'doctor': doctor})
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('home')

@login_required
def doctor_schedule(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        appointments = doctor.appointments.filter(status='SCHEDULED').order_by('appointment_date', 'appointment_time')
        return render(request, 'doctors/doctor_schedule.html', {
            'doctor': doctor,
            'appointments': appointments
        })
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('home')
