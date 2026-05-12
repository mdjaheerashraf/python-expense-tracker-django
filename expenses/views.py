from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from io import BytesIO
import base64


def home(request):

    expenses = Expense.objects.all()

    total = sum(expense.amount for expense in expenses)

    return render(request, 'home.html', {
        'expenses': expenses,
        'total': total
    })


def add_expense(request):

    if request.method == 'POST':

        form = ExpenseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {
        'form': form
    })


def edit_expense(request, id):

    expense = get_object_or_404(Expense, id=id)

    if request.method == 'POST':

        form = ExpenseForm(request.POST, instance=expense)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'add_expense.html', {
        'form': form
    })


def expense_chart(request):

    expenses = Expense.objects.all()

    categories = {}

    for expense in expenses:

        if expense.category in categories:
            categories[expense.category] += expense.amount

        else:
            categories[expense.category] = expense.amount

    labels = categories.keys()
    values = categories.values()

    plt.figure(figsize=(5,5))

    if values:
        plt.pie(values, labels=labels, autopct='%1.1f%%')

    buffer = BytesIO()

    plt.savefig(buffer, format='png')

    buffer.seek(0)

    image_png = buffer.getvalue()

    graph = base64.b64encode(image_png).decode('utf-8')

    buffer.close()

    return render(request, 'chart.html', {
        'graph': graph
    })