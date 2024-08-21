from django import forms
from .models import Goals


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goals
        fields = ['name', 'description', 'target_amount', 'due_date']
