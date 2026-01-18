from django.shortcuts import render

# Create your views here.
# courses/views.py
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from faculty.models import FacultyMember
from .models import Course, Enrollment, Grade
from .forms import GradeForm

class EnterGradesView(LoginRequiredMixin, FormView):
    template_name = 'courses/enter_grades.html'
    form_class = GradeForm

    def dispatch(self, request, *args, **kwargs):
        # Only faculty can access
        if request.user.role != 'faculty':
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_course(self):
        return get_object_or_404(Course, id=self.kwargs['course_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_course()
        faculty = get_object_or_404(FacultyMember, user=self.request.user)
        
        # Ensure faculty teaches this course
        if course.instructor != faculty:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You don't teach this course.")
        
        # Get all active enrollments for this course
        enrollments = Enrollment.objects.filter(course=course, status='active')
        grades_data = []
        for enrollment in enrollments:
            grade_obj, created = Grade.objects.get_or_create(enrollment=enrollment)
            grades_data.append({
                'student': enrollment.student,
                'enrollment_id': enrollment.id,
                'form': GradeForm(instance=grade_obj, prefix=f"grade_{enrollment.id}")
            })
        
        context['course'] = course
        context['grades_data'] = grades_data
        return context

    def post(self, request, *args, **kwargs):
        course = self.get_course()
        faculty = get_object_or_404(FacultyMember, user=request.user)
        if course.instructor != faculty:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied

        enrollments = Enrollment.objects.filter(course=course, status='active')
        all_valid = True
        forms = []

        for enrollment in enrollments:
            form = GradeForm(
                request.POST,
                instance=Grade.objects.get_or_create(enrollment=enrollment)[0],
                prefix=f"grade_{enrollment.id}"
            )
            forms.append((enrollment, form))
            if not form.is_valid():
                all_valid = False

        if all_valid:
            for enrollment, form in forms:
                form.save()
            messages.success(request, "Grades saved successfully!")
            return redirect('faculty_dashboard')
        else:
            # Re-render with errors
            context = self.get_context_data()
            context['grades_data'] = [
                {
                    'student': enrollment.student,
                    'enrollment_id': enrollment.id,
                    'form': form
                }
                for enrollment, form in forms
            ]
            return self.render_to_response(context)