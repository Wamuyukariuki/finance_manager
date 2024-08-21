from django.urls import path
from . import views

urlpatterns = [
    path('add_investment/', views.add_investment, name='add_investment'),
    path('investment_list/', views.investment_list, name='investment_list'),
    path('update_investment/<int:pk>/', views.update_investment, name='update_investment'),
    path('delete_investment/<int:pk>/', views.delete_investment, name='delete_investment'),
]
