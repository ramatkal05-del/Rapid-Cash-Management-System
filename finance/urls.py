from django.urls import path
from . import views

urlpatterns = [
    path('depenses/', views.expense_list, name='expense_list'),
    path('depenses/<int:expense_id>/', views.expense_detail, name='expense_detail'),
    path('depenses/ajouter/', views.create_expense, name='create_expense'),
    path('commissions/', views.commissions_list, name='commissions_list'),
]
