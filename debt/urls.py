from django.urls import path
from . import views

urlpatterns = [
    path('debts/', views.debt_list, name='debt_list'),
    path('add/', views.add_debt, name='add_debt'),
    path('edit-debt/<int:id>/', views.edit_debt, name='edit_debt'),
    path('delete-debt/<int:id>/', views.delete_debt, name='delete_debt'),
]
