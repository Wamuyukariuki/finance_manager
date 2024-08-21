from django import forms
from .models import Debt


class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['amount', 'description', 'due_date', 'is_paid', 'amount_paid']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
