from django.shortcuts import render

# Create your views here.
# faculty/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import FacultyMember
from courses.models import Course

class FacultyDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'faculty/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculty = get_object_or_404(FacultyMember, user=self.request.user)
        courses = Course.objects.filter(instructor=faculty)
        context['faculty'] = faculty
        context['courses'] = courses
        return context