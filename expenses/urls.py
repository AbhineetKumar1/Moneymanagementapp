"""splitmoney URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expense/', views.add_expense, name='add-expenses'),
    path('edit-expense/<int:id>/', views.edit_expense, name='expense-edit'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete-expense'),
    path('search-expenses/', views.search_expenses, name='search_expenses'),
    path('split-expense/', views.split_expense_list, name='split-expense-list'),
    path('split-expense/<int:expense_id>/', views.split_expense, name='split-expense'),
]