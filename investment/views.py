from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Investment
from .form import InvestmentForm


@login_required
def add_investment(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.user = request.user
            investment.save()
            return redirect('dashboard')  # redirect to a relevant page after saving
    else:
        form = InvestmentForm()
    return render(request, 'investment/add_investment.html', {'form': form})


@login_required
def investment_list(request):
    investments = Investment.objects.filter(user=request.user)
    return render(request, 'investment/investment_list.html', {'investments': investments})
