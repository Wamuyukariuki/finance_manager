from django.urls import path
from . import views

urlpatterns = [
    path('', views.savings_list, name='savings_list'),
    path('add/', views.savings_create, name='add_saving'),
    path('edit/<int:pk>/', views.savings_edit, name='update_saving'),
    path('delete/<int:pk>/', views.savings_delete, name='delete_saving'),
]
