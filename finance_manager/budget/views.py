from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum
from debt.models import Debt
from goals.models import Goals
from income.models import Income
from investment.models import Investment
from savings.models import Saving
from .forms import ExpenseForm, SignUpForm
from .models import Expense


@login_required
def dashboard(request):
    try:
        total_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_investments = Investment.objects.filter(user=request.user).aggregate(Sum('current_value'))[
                                'current_value__sum'] or 0
        total_expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_debts = Debt.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        total_savings = Saving.objects.filter(user=request.user).aggregate(Sum('current_amount'))[
                            'current_amount__sum'] or 0
        goals = Goals.objects.filter(user=request.user)

        context = {
            'total_income': total_income,
            'total_investments': total_investments,
            'total_expenses': total_expenses,
            'total_debts': total_debts,
            'total_savings': total_savings,
            'goals': goals,
        }
        return render(request, 'budget/dashboard.html', context)
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return render(request, 'budget/dashboard.html', {})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard directly after signup
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'budget/expense_list.html', {'expenses': expenses})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully.')
            return redirect('expense_list')
        else:
            messages.error(request, 'Error adding expense. Please check the form.')
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'budget/add_expense.html', {'form': form})


@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'budget/expense_create.html', {'form': form})
