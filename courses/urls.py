# courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('enter-grades/<int:course_id>/', views.EnterGradesView.as_view(), name='enter_grades'),
]