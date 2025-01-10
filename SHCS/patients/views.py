from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Patient
from appointments.models import Appointment

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 10

    def get_queryset(self):
        queryset = Patient.objects.filter(is_active=True)
        search_term = self.request.GET.get('search', '')
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        return queryset

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = self.object.appointments.all().order_by('-appointment_date')[:5]
        return context

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    template_name = 'patients/patient_form.html'
    fields = ['name', 'date_of_birth', 'gender', 'blood_group', 'contact_number', 
              'email', 'address', 'emergency_contact_name', 'emergency_contact_number',
              'medical_history', 'allergies', 'current_medications']
    success_url = reverse_lazy('patient_list')

    def form_valid(self, form):
        messages.success(self.request, 'Patient created successfully.')
        return super().form_valid(form)

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    template_name = 'patients/patient_form.html'
    fields = ['name', 'contact_number', 'email', 'address', 'emergency_contact_name',
              'emergency_contact_number', 'medical_history', 'allergies', 'current_medications']
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Patient information updated successfully.')
        return super().form_valid(form)

@login_required
def patient_history(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.all().order_by('-appointment_date')
    return render(request, 'patients/patient_history.html', {
        'patient': patient,
        'appointments': appointments
    })
