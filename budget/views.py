import logging
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from debt.models import Debt
from goals.models import Goals
from income.models import UserProfile, Income
from investment.models import Investment
from savings.models import Saving
from .forms import SignUpForm, ExpenseForm
from .models import Expense

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    try:
        now = timezone.now()
        start_of_month = now.replace(day=1)
        end_of_month = start_of_month + relativedelta(months=1, days=-1)

        user_profile = UserProfile.objects.get(user=request.user)

        # Query for financial metrics
        total_income = Income.objects.filter(user=request.user, date__range=(start_of_month, end_of_month)) \
                           .aggregate(total=Sum('amount'))['total'] or 0
        total_investments = Investment.objects.filter(user=request.user, date__range=(start_of_month, end_of_month)) \
                                .aggregate(total=Sum('current_value'))['total'] or 0
        total_expenses = Expense.objects.filter(user=request.user, date__range=(start_of_month, end_of_month)) \
                             .aggregate(total=Sum('amount'))['total'] or 0
        total_debts = Debt.objects.filter(user=request.user, due_date__range=(start_of_month, end_of_month)) \
                          .aggregate(total=Sum('amount'))['total'] or 0
        total_savings = Saving.objects.filter(user=request.user, start_date__range=(start_of_month, end_of_month)) \
                            .aggregate(total=Sum('current_amount'))['total'] or 0

        # Calculate budget recommendations
        needs_budget = user_profile.income * user_profile.needs_percentage / 100
        wants_budget = user_profile.income * user_profile.wants_percentage / 100
        savings_budget = user_profile.income * user_profile.savings_percentage / 100

        # Calculate financial standing
        total_spent = total_expenses + total_debts
        financial_standing = total_income - total_spent
        is_deficit = financial_standing < 0
        deficit_amount = abs(financial_standing) if is_deficit else 0

        # Calculate remaining goals if needed
        total_goals_target = Goals.objects.filter(user=request.user).aggregate(total=Sum('target_amount'))['total'] or 0
        remaining_goals = total_goals_target - total_savings

        context = {
            'total_income': total_income,
            'total_investments': total_investments,
            'total_expenses': total_expenses,
            'total_debts': total_debts,
            'total_savings': total_savings,
            'goals': Goals.objects.filter(user=request.user),
            'start_of_month': start_of_month,
            'end_of_month': end_of_month,
            'needs_budget': needs_budget,
            'wants_budget': wants_budget,
            'savings_budget': savings_budget,
            'financial_standing': financial_standing,
            'is_deficit': is_deficit,
            'deficit_amount': deficit_amount,
            'remaining_goals': remaining_goals,
        }

        return render(request, 'budget/dashboard.html', context)

    except UserProfile.DoesNotExist:
        messages.error(request, "UserProfile does not exist for the current user.")
        logger.error("Error in dashboard view: UserProfile matching query does not exist.")
        return redirect('profile_setup')

    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        logger.error(f"Error in dashboard view: {str(e)}")
        return render(request, 'budget/dashboard.html', {})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Error during login after signup.')
                return redirect('signup')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def expense_list(request):
    try:
        now = timezone.now()
        start_of_month = now.replace(day=1)
        end_of_month = start_of_month + relativedelta(months=1, days=-1)

        expenses = Expense.objects.filter(user=request.user, date__range=(start_of_month, end_of_month))

        paginator = Paginator(expenses, 10)  # Show 10 expenses per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        context = {
            'page_obj': page_obj,
            'total_expenses': total_expenses,
        }
        return render(request, 'budget/expense_list.html', context)

    except Exception as e:
        messages.error(request, f"Error loading expenses: {str(e)}")
        logger.error(f"Error in expense_list view: {str(e)}")
        return render(request, 'budget/expense_list.html', {})


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
def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense, user=request.user)
    return render(request, 'budget/update_expense.html', {'form': form})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully.')
        return redirect('expense_list')
    return render(request, 'budget/delete_expense.html', {'expense': expense})

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')
