from django.contrib import admin
from .models import Patient

# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'blood_group', 'contact_number', 'email', 'is_active')
    list_filter = ('gender', 'blood_group', 'is_active', 'created_at')
    search_fields = ('name', 'email', 'contact_number', 'emergency_contact_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'date_of_birth', 'gender', 'blood_group')
        }),
        ('Contact Information', {
            'fields': ('contact_number', 'email', 'address')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_number')
        }),
        ('Medical Information', {
            'fields': ('medical_history', 'allergies', 'current_medications'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def age(self, obj):
        return obj.age()
    age.short_description = 'Age'
