# students/views.py
from django.views.generic import CreateView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Student
from .forms import StudentForm
from accounts.decorators import role_required
from courses.models import Enrollment, Grade
from reports.utils import generate_transcript


# === Admin: Create Student ===
def admin_required(view_func):
    @login_required
    @role_required(['admin'])
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper


@method_decorator(admin_required, name='dispatch')
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = '/'


# === Student: Dashboard View ===
class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'students/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, user=self.request.user)
        enrollments = Enrollment.objects.filter(student=student)
        
        # Add grades
        enriched_enrollments = []
        for e in enrollments:
            try:
                grade = e.grade  # reverse OneToOne relation
            except Grade.DoesNotExist:
                grade = None
            enriched_enrollments.append({
                'enrollment': e,
                'grade': grade
            })
        
        context['student'] = student
        context['enriched_enrollments'] = enriched_enrollments
        return context


class TranscriptPDFView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        pdf = generate_transcript(student)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="transcript_{student.student_id}.pdf"'
        return response