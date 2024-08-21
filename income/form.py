from .models import Income
from django import forms
from .models import UserProfile


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'category', 'description']
        labels = {
            'amount': 'Amount',
            'date': 'Date',
            'category': 'Category',
            'description': 'Description',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['income', 'needs_percentage', 'wants_percentage', 'savings_percentage']
