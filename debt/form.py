from django import forms
from .models import Debt


class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['description', 'amount']  # Fields from your Debt model you want in the form
        labels = {
            'description': 'Description',
            'amount': 'Amount',
        }
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize any additional form initialization here if needed
