# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.StudentCreateView.as_view(), name='student_add'),
    path('dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('transcript/', views.TranscriptPDFView.as_view(), name='student_transcript'),
]