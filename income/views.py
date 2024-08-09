from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .form import IncomeForm
from .models import Income


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


@login_required
def edit_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)

    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income_list')  # Redirect to a relevant page after saving
        else:
            print(form.errors)  # Debugging statement to check for form errors
    else:
        form = IncomeForm(instance=income)

    return render(request, 'income/edit_income.html', {'form': form})
