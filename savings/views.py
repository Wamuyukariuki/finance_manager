from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .forms import SavingForm
from .models import Saving

@login_required
def savings_list(request):
    # Retrieve savings for the current user
    savings = Saving.objects.filter(user=request.user)

    # Calculate total savings amount for the current user
    total_savings = savings.aggregate(Sum('current_amount'))['current_amount__sum'] or 0

    context = {
        'savings': savings,
        'total_savings': total_savings,
    }

    return render(request, 'savings/savings_list.html', context)


@login_required
def savings_create(request):
    if request.method == 'POST':
        form = SavingForm(request.POST)
        if form.is_valid():
            saving = form.save(commit=False)
            saving.user = request.user
            saving.save()
            return redirect('savings_list')
    else:
        form = SavingForm()
    return render(request, 'savings/savings_form.html', {'form': form})


@login_required
def savings_edit(request, pk):
    saving = get_object_or_404(Saving, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SavingForm(request.POST, instance=saving)
        if form.is_valid():
            form.save()
            return redirect('savings_list')
    else:
        form = SavingForm(instance=saving)
    return render(request, 'savings/savings_form.html', {'form': form})


@login_required
def savings_delete(request, pk):
    saving = get_object_or_404(Saving, pk=pk, user=request.user)
    if request.method == 'POST':
        saving.delete()
        return redirect('savings_list')
    return render(request, 'savings/savings_confirm_delete.html', {'saving': saving})
