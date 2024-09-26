import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta


import logging

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from goals.views import calculate_total_goals, calculate_remaining_goals

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
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = (start_of_month + timezone.timedelta(days=31)).replace(day=1) - timezone.timedelta(seconds=1)

        user_profile = UserProfile.objects.get(user=request.user)

        # Query for financial metrics (monthly)
        metrics = {
            'total_income': Income.objects.filter(user=request.user, date__range=(start_of_month, end_of_month)).aggregate(total=Sum('amount'))['total'] or 0,
            'total_investments': Investment.objects.filter(user=request.user, date__range=(start_of_month, end_of_month)).aggregate(total=Sum('current_value'))['total'] or 0,
            'total_expenses': Expense.objects.filter(user=request.user, date__range=(start_of_month, end_of_month)).aggregate(total=Sum('amount'))['total'] or 0,
            'total_debts': Debt.objects.filter(user=request.user, due_date__range=(start_of_month, end_of_month)).aggregate(total=Sum('amount'))['total'] or 0,
            'total_savings': Saving.objects.filter(user=request.user, start_date__range=(start_of_month, end_of_month)).aggregate(total=Sum('current_amount'))['total'] or 0,
        }

        # Calculate budget recommendations
        income = user_profile.income
        needs_budget = income * user_profile.needs_percentage / 100
        wants_budget = income * user_profile.wants_percentage / 100
        savings_budget = income * user_profile.savings_percentage / 100

        # Calculate financial standing
        total_spent = metrics['total_expenses'] + metrics['total_debts']
        financial_standing = metrics['total_income'] - total_spent
        is_deficit = financial_standing < 0
        deficit_amount = abs(financial_standing) if is_deficit else 0

        # Calculate total and remaining goals (long-term)
        total_goals_target = calculate_total_goals(request.user)
        remaining_goals = calculate_remaining_goals(request.user, metrics['total_savings'])

        context = {
            **metrics,
            'goals': Goals.objects.filter(user=request.user),
            'needs_budget': needs_budget,
            'wants_budget': wants_budget,
            'savings_budget': savings_budget,
            'financial_standing': financial_standing,
            'is_deficit': is_deficit,
            'deficit_amount': deficit_amount,
            'total_goals_target': total_goals_target,
            'remaining_goals': remaining_goals,
        }

        return render(request, 'budget/dashboard.html', context)

    except UserProfile.DoesNotExist:
        messages.error(request, "UserProfile does not exist for the current user.")
        return redirect('profile_setup')

    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return render(request, 'budget/dashboard.html', {})


@login_required
def download_report(request, year, month):
    # Create the response object for the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="financial_report_{year}_{month}.pdf"'

    # Create the PDF object
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title and User info
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Financial Report")
    p.setFont("Helvetica", 12)
    p.drawString(100, 780, f"User: {request.user.username}")
    p.drawString(100, 765, f"Month: {month} Year: {year}")

    # Initialize Y position for text placement
    y_position = 740
    line_height = 15

    # Determine the start and end of the specified month
    start_of_month = timezone.datetime(year, month, 1)
    end_of_month = start_of_month + relativedelta(months=1, days=-1)

    # Fetch user data for the specified month
    expenses = Expense.objects.filter(user=request.user, date__range=[start_of_month, end_of_month])
    debts = Debt.objects.filter(user=request.user, due_date__range=[start_of_month, end_of_month])
    savings = Saving.objects.filter(user=request.user)  # Filtered without date range
    goals = Goals.objects.filter(user=request.user)  # Filtered without date range

    def check_page_overflow(p, y_position):
        if y_position <= 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            return 800
        return y_position

    # Display Expenses Section
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y_position, "Expenses:")
    y_position -= line_height
    p.setFont("Helvetica", 12)
    for expense in expenses:
        p.drawString(100, y_position, f"- {expense.category}: KES {expense.amount:,.2f}")
        y_position -= line_height
        y_position = check_page_overflow(p, y_position)

    # Display Debts Section
    y_position -= 10
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y_position, "Debts:")
    y_position -= line_height
    p.setFont("Helvetica", 12)
    for debt in debts:
        p.drawString(100, y_position, f"- {debt.description}: KES {debt.amount:,.2f}")
        y_position -= line_height
        y_position = check_page_overflow(p, y_position)

    # Display Savings Section
    y_position -= 10
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y_position, "Savings:")
    y_position -= line_height
    p.setFont("Helvetica", 12)
    for saving in savings:
        p.drawString(100, y_position, f"- {saving.name}: KES {saving.current_amount:,.2f}")
        y_position -= line_height
        y_position = check_page_overflow(p, y_position)

    # Display Goals Section
    y_position -= 10
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y_position, "Goals:")
    y_position -= line_height
    p.setFont("Helvetica", 12)
    for goal in goals:
        p.drawString(100, y_position, f"- {goal.name}: Target KES {goal.target_amount:,.2f}")
        y_position -= line_height
        y_position = check_page_overflow(p, y_position)

    # Finalize the PDF
    p.showPage()
    p.save()

    return response



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
        year = int(request.GET.get('year', now.year))
        month = int(request.GET.get('month', now.month))

        start_of_month, end_of_month = get_start_and_end_of_month(year, month)

        expenses = Expense.objects.filter(user=request.user, date__range=(start_of_month, end_of_month))
        paginator = Paginator(expenses, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        context = {
            'page_obj': page_obj,
            'total_expenses': total_expenses,
            'year': year,
            'month': month,
        }

        return render(request, 'budget/expense_list.html', context)

    except Exception as e:
        logger.error(f"Error loading expenses: {str(e)}")
        messages.error(request, "An error occurred while loading expenses. Please try again later.")
        return render(request, 'budget/expense_list.html', {'error': 'Unable to load expenses.'})

def get_start_and_end_of_month(year, month):
    start_of_month = timezone.make_aware(datetime(year, month, 1))
    last_day = calendar.monthrange(year, month)[1]
    end_of_month = timezone.make_aware(datetime(year, month, last_day, 23, 59, 59))
    return start_of_month, end_of_month


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Associate the expense with the logged-in user
            expense.save()
            messages.success(request, 'Expense added successfully.')
            return redirect('expense_list')  # Redirect to the expense list
        else:
            messages.error(request, 'Error adding expense. Please check the form.')
    else:
        form = ExpenseForm(user=request.user)  # Initialize an empty form for GET requests

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
            messages.error(request, 'Error updating expense. Please check the form.')
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