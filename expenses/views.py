from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = 'USD'  # Default currency if user preference doesn't exist
    
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)

        expense = Expense.objects.create(
            owner=request.user, 
            amount=amount, 
            date=date,
            category=category, 
            description=description
        )

        if 'split' in request.POST:
            return redirect('split-expense', expense_id=expense.id)

        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')

@login_required(login_url='/authentication/login')
def edit_expense(request, id):
    expense = get_object_or_404(Expense, pk=id, owner=request.user)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_expense.html', context)
        
        expense.amount = amount
        expense.description = description
        expense.date = date
@login_required(login_url='/authentication/login')
def split_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id, owner=request.user)
    if request.method == 'POST':
        num_people = int(request.POST.get('num_people', 2))
        if num_people < 2:
            messages.error(request, 'You need at least 2 people to split an expense.')
            return render(request, 'expenses/split_expense.html', {'expense': expense})
        
        split_amount = expense.amount / num_people
        
        # Create new expenses for each split
        for i in range(num_people - 1):  # -1 because the original expense counts as one
            Expense.objects.create(
                amount=split_amount,
                category=expense.category,
                description=f"Split of {expense.description}",
                owner=request.user,
                date=expense.date
            )
        
        # Update the original expense
        expense.amount = split_amount
        expense.description = f"{expense.description} (Split {num_people} ways)"
        expense.save()
        
        messages.success(request, f'Expense split {num_people} ways successfully')
        return redirect('expenses')
    
    return render(request, 'expenses/split_expense.html', {'expense': expense})

@login_required(login_url='/authentication/login')
def split_expense_list(request):
    split_expenses = Expense.objects.filter(owner=request.user, description__contains='(Split')
    return render(request, 'expenses/split_expense_list.html', {'split_expenses': split_expenses})

@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = get_object_or_404(Expense, pk=id, owner=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense removed')
        return redirect('expenses')
    return render(request, 'expenses/delete_expense.html', {'expense': expense})        