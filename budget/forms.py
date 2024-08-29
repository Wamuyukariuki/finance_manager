from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Expense, ExpenseCategory

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description']
        widgets = {
            'category': forms.Select(choices=[(c.id, c.name) for c in ExpenseCategory.objects.all()]),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = ExpenseCategory.objects.all()
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 4})


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
