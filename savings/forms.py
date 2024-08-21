from django import forms
from .models import Saving

class SavingForm(forms.ModelForm):
    class Meta:
        model = Saving
        fields = ['name', 'target_amount', 'current_amount', 'start_date', 'due_date', 'description']
