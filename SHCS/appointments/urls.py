from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='appointment_list'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('create/', views.create_appointment, name='create_appointment'),
    path('<int:pk>/update-status/', views.update_appointment_status, name='update_appointment_status'),
    path('doctor/', views.doctor_appointments, name='doctor_appointments'),
    path('patient/<int:patient_id>/', views.patient_appointments, name='patient_appointments'),
]
