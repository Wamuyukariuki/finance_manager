from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from dateutil.relativedelta import relativedelta  # Import relativedelta

from .form import DebtForm
from .models import Debt

def calculate_total_debts(user):
    """Calculate total debts for the current user in the current month."""
    now = timezone.now()
    start_of_month = now.replace(day=1)
    end_of_month = start_of_month + relativedelta(months=1, days=-1)

    total_debts = Debt.objects.filter(user=user, due_date__range=(start_of_month, end_of_month)).aggregate(Sum('amount'))['amount__sum'] or 0
    return total_debts

@login_required
def add_debt(request):
    if request.method == 'POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.user = request.user  # Assign the current user to the debt
            debt.save()
            return redirect('debt_list')  # Redirect to the list of debts
    else:
        form = DebtForm()
    return render(request, 'debt/debt_form.html', {'form': form})

@login_required
def debt_list(request):
    # Get current date and the start and end of the current month
    now = timezone.now()
    start_of_month = now.replace(day=1)
    end_of_month = start_of_month + relativedelta(months=1, days=-1)

    # Filter debts for the current month using 'due_date'
    debts = Debt.objects.filter(user=request.user, due_date__gte=start_of_month, due_date__lte=end_of_month)

    # Calculate total debts for the current month
    total_debts = debts.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'debts': debts,
        'total_debts': total_debts,
    }
    return render(request, 'debt/debt_list.html', context)

@login_required
def edit_debt(request, pk):
    debt = get_object_or_404(Debt, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DebtForm(request.POST, instance=debt)
        if form.is_valid():
            form.save()
            return redirect('debt_list')
    else:
        form = DebtForm(instance=debt)
    return render(request, 'debt/edit_debt.html', {'form': form})


@login_required
def delete_debt(request, pk):
    debt = get_object_or_404(Debt, pk=pk, user=request.user)  # Ensure debt belongs to current user

    if request.method == 'POST':
        debt.delete()
        return redirect('debt_list')  # Redirect to the debt list after deletion

    return render(request, 'debt/delete_debt.html', {'debt': debt})
