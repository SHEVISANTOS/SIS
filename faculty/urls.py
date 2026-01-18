# faculty/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.FacultyDashboardView.as_view(), name='faculty_dashboard'),
]