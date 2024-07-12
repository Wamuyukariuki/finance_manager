from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('expenses/', views.expense_list, name='expense_list'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('expenses/create/', views.expense_create, name='expense_create'),
]
