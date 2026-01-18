from django.db import models

# Create your models here.
# faculty/models.py
from django.db import models
from django.conf import settings

class FacultyMember(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"