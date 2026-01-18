# courses/forms.py
from django import forms
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['midterm', 'final_exam']
        widgets = {
            'midterm': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.01}),
            'final_exam': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.01}),
        }

    def clean_midterm(self):
        score = self.cleaned_data.get('midterm')
        if score is not None and (score < 0 or score > 100):
            raise forms.ValidationError("Midterm must be between 0 and 100.")
        return score

    def clean_final_exam(self):
        score = self.cleaned_data.get('final_exam')
        if score is not None and (score < 0 or score > 100):
            raise forms.ValidationError("Final exam must be between 0 and 100.")
        return score