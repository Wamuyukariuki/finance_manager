from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .form import GoalForm
from .models import Goals
from django.db.models import Sum

def calculate_total_goals(user):
    """Calculate total target amount for all goals for the current user."""
    total_goals_target = Goals.objects.filter(user=user).aggregate(Sum('target_amount'))['target_amount__sum'] or 0
    return total_goals_target

def calculate_remaining_goals(user, total_savings):
    """Calculate the remaining amount to reach all goals based on the current savings."""
    total_goals_target = calculate_total_goals(user)
    remaining_goals = total_goals_target - total_savings
    return remaining_goals

@login_required
def goals_list(request):
    now = timezone.now()
    start_of_month = now.replace(day=1)
    end_of_month = start_of_month + relativedelta(months=1, days=-1)

    goals_list = Goals.objects.filter(
        user=request.user,
        created_at__gte=start_of_month,
        created_at__lte=end_of_month
    ).order_by('created_at')

    paginator = Paginator(goals_list, 10)  # Show 10 goals per page
    page_number = request.GET.get('page')
    goals = paginator.get_page(page_number)

    # Optimize queries by storing results in variables
    total_target_amount = goals_list.aggregate(Sum('target_amount'))['target_amount__sum'] or 0
    total_amount_saved = goals_list.aggregate(Sum('amount_saved'))['amount_saved__sum'] or 0

    context = {
        'goals': goals,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
        'total_target_amount': total_target_amount,
        'total_amount_saved': total_amount_saved,
    }

    if not goals_list.exists():
        messages.info(request, 'No goals found for this month.')

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
