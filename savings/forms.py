from django import forms
from django.forms import DateInput
from .models import Saving

class SavingForm(forms.ModelForm):
    class Meta:
        model = Saving
        fields = ['name', 'target_amount', 'current_amount', 'start_date', 'due_date', 'description']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'due_date': DateInput(attrs={'type': 'date'}),
        }
