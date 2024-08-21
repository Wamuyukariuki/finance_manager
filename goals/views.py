from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from .models import Goals
from .form import GoalForm
from django.shortcuts import render
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import Goals
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def goals_list(request):
    now = timezone.now()
    start_of_month = now.replace(day=1)
    end_of_month = start_of_month + relativedelta(months=1, days=-1)

    goals_list = Goals.objects.filter(user=request.user, created_at__gte=start_of_month, created_at__lte=end_of_month)

    paginator = Paginator(goals_list, 10)  # Show 10 goals per page
    page_number = request.GET.get('page')
    goals = paginator.get_page(page_number)

    context = {
        'goals': goals,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
    }

    return render(request, 'goals/goals_list.html', context)


@login_required
def goal_create(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user  # Assign the current user to the goal
            goal.save()
            messages.success(request, 'Goal created successfully.')
            return redirect('goals_list')
        else:
            messages.error(request, 'Error creating goal. Please check the form.')
    else:
        form = GoalForm()
    return render(request, 'goals/goal_form.html', {'form': form})


@login_required
def goal_edit(request, id):
    goal = get_object_or_404(Goals, id=id)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goal updated successfully.')
            return redirect('goals_list')
        else:
            messages.error(request, 'Error updating goal. Please check the form.')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goals/goal_form.html', {'form': form})


@login_required
def goal_delete(request, id):
    goal = get_object_or_404(Goals, id=id)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted successfully.')
        return redirect('goals_list')
    return render(request, 'goals/goal_confirm_delete.html', {'goal': goal})
