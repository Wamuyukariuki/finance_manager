from django.urls import path
from . import views

urlpatterns = [
    path('', views.savings_list, name='savings_list'),  # Correct URL name
    path('create/', views.savings_create, name='savings_create'),
    path('<int:pk>/edit/', views.savings_edit, name='savings_edit'),
    path('<int:pk>/delete/', views.savings_delete, name='savings_delete'),
]
