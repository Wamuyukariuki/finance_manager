from django.shortcuts import render, get_object_or_404, redirect
from .models import Saving
from .forms import SavingForm  # Assuming you have a form for creating/editing savings

def savings_list(request):
    savings = Saving.objects.filter(user=request.user)
    return render(request, 'savings/savings_list.html', {'savings': savings})

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

def savings_delete(request, pk):
    saving = get_object_or_404(Saving, pk=pk, user=request.user)
    if request.method == 'POST':
        saving.delete()
        return redirect('savings_list')
    return render(request, 'savings/savings_confirm_delete.html', {'saving': saving})
