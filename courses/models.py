# courses/models.py
from django.db import models
from students.models import Student
from faculty.models import FacultyMember
from decimal import Decimal 

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    credits = models.PositiveSmallIntegerField(default=3)
    department = models.CharField(max_length=100, default="General")
    instructor = models.ForeignKey(
        FacultyMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  # ← MUST BE HERE

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} → {self.course}"
    
class Grade(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    midterm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    final_exam = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    letter_grade = models.CharField(max_length=2, blank=True)

    def save(self, *args, **kwargs):
        if self.midterm is not None and self.final_exam is not None:
            self.total = (self.midterm * Decimal('0.4')) + (self.final_exam * Decimal('0.6'))
            if self.total >= Decimal('90'):
                self.letter_grade = 'A'
            elif self.total >= Decimal('80'):
                self.letter_grade = 'B'
            elif self.total >= Decimal('70'):
                self.letter_grade = 'C'
            elif self.total >= Decimal('60'):
                self.letter_grade = 'D'
            else:
                self.letter_grade = 'F'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.enrollment.student} - {self.enrollment.course}: {self.letter_grade}"