from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'appointment_date', 
                   'appointment_time', 'status', 'priority')
    list_filter = ('status', 'priority', 'appointment_date', 'doctor')
    search_fields = ('patient__name', 'doctor__user__first_name', 
                    'doctor__user__last_name', 'reason')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'appointment_date'
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'appointment_date', 'appointment_time')
        }),
        ('Medical Information', {
            'fields': ('reason', 'symptoms', 'priority')
        }),
        ('Status and Follow-up', {
            'fields': ('status', 'notes', 'prescription', 'follow_up_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_patient_name(self, obj):
        return obj.patient.name
    get_patient_name.short_description = 'Patient'

    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.get_full_name()}"
    get_doctor_name.short_description = 'Doctor'

    def save_model(self, request, obj, form, change):
        if not change:  # Only for new appointments
            obj.clean()  # Run validation
        super().save_model(request, obj, form, change)
