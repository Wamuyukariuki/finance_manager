from django.shortcuts import render, get_object_or_404, redirect
from .models import Goals
from .form import GoalForm


def goals_list(request):
    goals = Goals.objects.filter(user=request.user)
    return render(request, 'goals/goals_list.html', {'goals': goals})


def goal_create(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goal_list')
    else:
        form = GoalForm()
    return render(request, 'goals/goal_form.html', {'form': form})


def goal_edit(request, id):
    goal = get_object_or_404(Goals, id=id)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goal_list')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goals/goal_form.html', {'form': form})
