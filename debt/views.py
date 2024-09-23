from dateutil.relativedelta import relativedelta  # Import relativedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils import timezone

from .form import DebtForm
from .models import Debt


@login_required
def debt_list(request):
    now = timezone.now()
    start_of_month = now.replace(day=1)
    end_of_month = start_of_month + relativedelta(months=1, days=-1)

    # Filter debts for the current month
    debts = Debt.objects.filter(user=request.user, due_date__gte=start_of_month, due_date__lte=end_of_month)

    # Calculate total debts and total paid
    total_debts = debts.aggregate(Sum('amount'))['amount__sum'] or 0
    total_amount_paid = debts.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

    # Calculate total outstanding balance
    total_outstanding_balance = sum(debt.outstanding_balance for debt in debts)

    context = {
        'debts': debts,
        'total_debts': total_debts,
        'total_amount_paid': total_amount_paid,
        'total_outstanding_balance': total_outstanding_balance,
    }
    return render(request, 'debt/debt_list.html', context)


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
