from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Debt
from django.shortcuts import render, redirect
from .form import DebtForm


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
    debts = Debt.objects.filter(user=request.user)
    context = {
        'debts': debts,
    }
    return render(request, 'debt/debt_list.html', context)


@login_required
def edit_debt(request, id):
    debt = get_object_or_404(Debt, id=id)
    if request.method == 'POST':
        form = DebtForm(request.POST, instance=debt)
        if form.is_valid():
            form.save()
            return redirect('debt_list')  # Adjust the redirect target as needed
    else:
        form = DebtForm(instance=debt)
    return render(request, 'debt/edit_debt.html', {'form': form})


@login_required
def delete_debt(request, id):
    debt = get_object_or_404(Debt, id=id)
    if request.method == 'POST':
        debt.delete()
        return redirect('debt_list')  # Adjust the redirect target as needed
    return render(request, 'debt/confirm_delete.html', {'debt': debt})
