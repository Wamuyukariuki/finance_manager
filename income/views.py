from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from .form import IncomeForm, UserProfileForm
from .models import Income, UserProfile


@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'income/add_income.html', {'form': form})


@login_required
def income_list(request):
    # Retrieve incomes for the current user
    incomes = Income.objects.filter(user=request.user)

    # Calculate total income for the current user
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'incomes': incomes,
        'total_income': total_income,
    }

    return render(request, 'income/income_list.html', context)


@login_required
def update_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'income/update_income.html', {'form': form})


@login_required
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        return redirect('income_list')
    return render(request, 'income/delete_income.html', {'income': income})


@login_required
def profile_setup(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile/profile_setup.html', {'form': form})
