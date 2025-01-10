from django.contrib import admin
from .models import Doctor

# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'specialization', 'license_number', 'contact_number', 'is_active')
    list_filter = ('specialization', 'is_active', 'available_days')
    search_fields = ('user__first_name', 'user__last_name', 'specialization', 'license_number')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'specialization', 'license_number', 'experience_years')
        }),
        ('Contact Details', {
            'fields': ('contact_number', 'address')
        }),
        ('Professional Details', {
            'fields': ('consultation_fee', 'is_active')
        }),
        ('Availability', {
            'fields': ('available_days', 'available_time_start', 'available_time_end')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_full_name(self, obj):
        return f"Dr. {obj.user.get_full_name()}"
    get_full_name.short_description = 'Doctor Name'
