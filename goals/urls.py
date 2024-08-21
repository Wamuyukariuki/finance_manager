from django.urls import path
from . import views

urlpatterns = [
    path('goals/', views.goals_list, name='goals_list'),
    path('goals/create/', views.goal_create, name='goal_create'),
    path('goals/edit/<int:id>/', views.goal_edit, name='goal_edit'),
    path('goals/delete/<int:id>/', views.goal_delete, name='goal_delete'),
]
