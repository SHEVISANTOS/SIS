from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FacultyMember

@admin.register(FacultyMember)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department')