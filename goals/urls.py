from django.urls import path
from . import views

urlpatterns = [
    path('', views.goals_list, name='goal_list'),
    path('new/', views.goal_create, name='goal_create'),
    path('edit/<int:id>/', views.goal_edit, name='goal_edit'),
]
