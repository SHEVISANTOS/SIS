from django.contrib import admin

# Register your models here.
# students/admin.py
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'date_of_birth')
    search_fields = ('student_id', 'user__username')