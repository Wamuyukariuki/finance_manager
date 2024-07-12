from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_investment, name='add_investment'),
    path('list/', views.investment_list, name='investment_list'),
]
