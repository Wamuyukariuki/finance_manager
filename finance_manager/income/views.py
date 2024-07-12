from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Income
from .form import IncomeForm


@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')  # redirect to a relevant page after saving
    else:
        form = IncomeForm()
    return render(request, 'income/add_income.html', {'form': form})


@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user)
    return render(request, 'income/income_list.html', {'incomes': incomes})
