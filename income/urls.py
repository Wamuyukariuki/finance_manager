from django.urls import path
from . import views

urlpatterns = [
    path('add_income/', views.add_income, name='add_income'),
    path('income_list/', views.income_list, name='income_list'),
    path('update_income/<int:pk>/', views.update_income, name='update_income'),
    path('delete_income/<int:pk>/', views.delete_income, name='delete_income'),
    path('profile_setup/', views.profile_setup, name='profile_setup'),
]
