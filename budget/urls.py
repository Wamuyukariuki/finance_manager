from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/create/', views.add_expense, name='expense_create'),
    path('expenses/<int:pk>/update/', views.update_expense, name='update_expense'),
    path('expenses/<int:pk>/delete/', views.delete_expense, name='delete_expense'),
    path('add/', views.add_expense, name='add_expense'),

    path('signup/', views.signup, name='signup'),  # Added signup URL

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
