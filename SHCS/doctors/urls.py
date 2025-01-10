from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctor_list'),
    path('<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('profile/', views.doctor_profile, name='doctor_profile'),
    path('schedule/', views.doctor_schedule, name='doctor_schedule'),
]
