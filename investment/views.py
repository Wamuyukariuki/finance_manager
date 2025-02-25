import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .form import InvestmentForm
from .models import Investment

from django.contrib import messages

# Configure logging
logger = logging.getLogger(__name__)

@login_required
def add_investment(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.user = request.user
            investment.save()
            messages.success(request, 'Investment added successfully!')
            return redirect('investment_list')
    else:
        form = InvestmentForm()

    return render(request, 'investment/add_investment.html', {'form': form})

@login_required
def investment_list(request):
    try:
        investments = Investment.objects.filter(user=request.user)
        logger.debug(f"Number of investments: {investments.count()}")

        total_investment = investments.aggregate(Sum('current_value'))['current_value__sum'] or 0
        logger.debug(f"Total investment value: {total_investment}")

        context = {
            'investments': investments,
            'total_investment': total_investment,
        }

        return render(request, 'investment/investment_list.html', context)

    except Exception as e:
        logger.error(f"Error in investment_list view: {str(e)}")
        messages.error(request, 'An error occurred while retrieving investments.')
        return render(request, 'investment/investment_list.html', {'investments': [], 'total_investment': 0})

@login_required
def update_investment(request, pk):
    investment = get_object_or_404(Investment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = InvestmentForm(request.POST, instance=investment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Investment updated successfully!')
            return redirect('investment_list')
    else:
        form = InvestmentForm(instance=investment)
    return render(request, 'investment/update_investment.html', {'form': form})

@login_required
def delete_investment(request, pk):
    investment = get_object_or_404(Investment, pk=pk, user=request.user)
    if request.method == 'POST':
        investment.delete()
        messages.success(request, 'Investment deleted successfully!')
        return redirect('investment_list')
    return render(request, 'investment/delete_investment.html', {'investment': investment})
