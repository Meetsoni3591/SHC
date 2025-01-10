from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from patients.models import Patient
from doctors.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show')
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('EMERGENCY', 'Emergency')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SCHEDULED')
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.appointment_date < timezone.now().date():
            raise ValidationError("Appointment date cannot be in the past")
        
        # Check if doctor is available on this day and time
        appointment_datetime = timezone.datetime.combine(
            self.appointment_date, 
            self.appointment_time
        ).time()
        
        if not self.is_doctor_available():
            raise ValidationError("Doctor is not available at this time")

    def is_doctor_available(self):
        # Convert appointment time to datetime for comparison
        appointment_datetime = timezone.datetime.combine(
            self.appointment_date, 
            self.appointment_time
        )
        
        # Check if the appointment falls within doctor's available hours
        if (self.appointment_time < self.doctor.available_time_start or 
            self.appointment_time > self.doctor.available_time_end):
            return False
            
        # Check if doctor has any other appointments at this time
        conflicting_appointments = Appointment.objects.filter(
            doctor=self.doctor,
            appointment_date=self.appointment_date,
            appointment_time=self.appointment_time,
            status__in=['SCHEDULED', 'CONFIRMED']
        ).exclude(pk=self.pk)
        
        return not conflicting_appointments.exists()

    def __str__(self):
        return f"{self.patient.name} - Dr. {self.doctor.user.get_full_name()} - {self.appointment_date}"

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
