# ==========================================
# IMPORTS
# ==========================================

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q, Sum, Avg
from datetime import date, datetime, timedelta

from .models import Expense
from .forms import ExpenseForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from collections import OrderedDict
# ==========================================
# MATPLOTLIB
# ==========================================

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from io import BytesIO
import base64

# ==========================================
# REPORTLAB
# ==========================================

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# ==========================================
# HOME PAGE
# ==========================================
@login_required
def home(request):

    # -----------------------------
    # Search & Filter
    # -----------------------------

    search_query = request.GET.get("search", "")
    category_filter = request.GET.get("category", "")
    month_filter = request.GET.get("month", "")
    year_filter = request.GET.get("year", "")

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by("-date", "-id")

    if search_query:

        expenses = expenses.filter(

            Q(title__icontains=search_query) |
            Q(category__icontains=search_query)

        )

    if category_filter:

        expenses = expenses.filter(
            category=category_filter
        )

    if month_filter:
        expenses = expenses.filter(
        date__month=month_filter
    )

    if year_filter:
        expenses = expenses.filter(
        date__year=year_filter
    )

    categories = (
    Expense.objects.filter(user=request.user)
    .values_list("category", flat=True)
    .distinct()
    )

    months = [

    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December"),

    ]

    years = (
        Expense.objects.filter(user=request.user)
        .dates("date", "year")
    )

    years = [d.year for d in years]

    # -----------------------------
    # Total Expense
    # -----------------------------

    total = sum(
        expense.amount
        for expense in expenses
    )

    # -----------------------------
    # Pie Chart
    # -----------------------------

    category_data = {}

    for expense in expenses:

        if expense.category in category_data:

            category_data[expense.category] += expense.amount

        else:

            category_data[expense.category] = expense.amount

    highest_category = "-"

    highest_amount = 0

    for category, amount in category_data.items():

        if amount > highest_amount:

            highest_amount = amount

        highest_category = category

    labels = list(category_data.keys())

    values = list(category_data.values())

    plt.figure(figsize=(5,5))

    if values:

        plt.pie(

            values,

            labels=labels,

            autopct="%1.1f%%"

        )

        plt.title("Expense Distribution")

    buffer = BytesIO()

    plt.savefig(

        buffer,

        format="png",

        bbox_inches="tight"

    )

    plt.close()

    buffer.seek(0)

    graph = base64.b64encode(

        buffer.getvalue()

    ).decode("utf-8")

    buffer.close()

    # -----------------------------
    # Dashboard Statistics
    # -----------------------------

    total_transactions = expenses.count()

    total_categories = (
    Expense.objects.filter(user=request.user)
    .values("category")
    .distinct()
    .count()
    )

    this_month_expense = sum(

        expense.amount

        for expense in expenses

        if expense.date.month == date.today().month

        and expense.date.year == date.today().year

    )

    # -----------------------------
    # Highest Spending Category
    # -----------------------------

    highest_category = "N/A"
    highest_amount = 0

    category_totals = {}

    for expense in expenses:

        category_totals[expense.category] = (
            category_totals.get(expense.category, 0)
            + expense.amount
        )

    if category_totals:

        highest_category = max(
            category_totals,
            key=category_totals.get
        )

        highest_amount = category_totals[highest_category]

     # -----------------------------
     # Biggest Expense
     # -----------------------------

    biggest_expense = expenses.order_by("-amount").first()

    # -----------------------------
    # Average Daily Expense
    # -----------------------------

    average_daily = 0

    if expenses.exists():

        total_days = (
            max(
                (date.today() - expense.date).days
                for expense in expenses
            ) + 1
        )

        average_daily = round(
            total / total_days,
            2
        )

    # -----------------------------
    # Dashboard Statistics
    # -----------------------------

    total_transactions = expenses.count()

    total_categories = (
        Expense.objects.filter(user=request.user)
        .values("category")
        .distinct()
        .count()
    )

    this_month_expense = sum(

        expense.amount

        for expense in expenses

        if expense.date.month == date.today().month

        and expense.date.year == date.today().year

    )

    from datetime import timedelta

    last_30_days = expenses.filter(
        date__gte=date.today() - timedelta(days=30)
    )

    last_30_total = sum(
        expense.amount
        for expense in last_30_days
    )

    last_30_transactions = last_30_days.count()

    average_daily_expense = round(
        last_30_total / 30,
        2
    )
    # -----------------------------
    # Last 30 Days Statistics
    # -----------------------------

    last_30_days = expenses.filter(
        date__gte=date.today() - timedelta(days=30)
    )

    last_30_total = sum(
        expense.amount
        for expense in last_30_days
    )

    last_30_transactions = last_30_days.count()


    # -----------------------------
    # Monthly Spending Chart
    # -----------------------------

    monthly_totals = OrderedDict([
        ("Jan", 0),
        ("Feb", 0),
        ("Mar", 0),
        ("Apr", 0),
        ("May", 0),
        ("Jun", 0),
        ("Jul", 0),
        ("Aug", 0),
        ("Sep", 0),
        ("Oct", 0),
        ("Nov", 0),
        ("Dec", 0),
    ])

    for expense in expenses:

        month = expense.date.strftime("%b")

        monthly_totals[month] += expense.amount

    plt.figure(figsize=(8, 4))

    plt.bar(
    monthly_totals.keys(),
    monthly_totals.values(),
    )

    plt.title("Monthly Spending")

    plt.xlabel("Month")

    plt.ylabel("Amount (₹)")

    plt.grid(axis="y", linestyle="--", alpha=0.4)

    monthly_buffer = BytesIO()

    plt.savefig(
        monthly_buffer,
        format="png",
        bbox_inches="tight"
    )

    plt.close()

    monthly_buffer.seek(0)

    monthly_graph = base64.b64encode(
        monthly_buffer.getvalue()
    ).decode("utf-8")

    monthly_buffer.close()

        # -----------------------------
        # Render
        # -----------------------------

    return render(

        request,

        "home.html",

        {

            "expenses": expenses,

            "total": total,

            "graph": graph,

            "search_query": search_query,

            "category_filter": category_filter,

            "categories": categories,

            "total_transactions": total_transactions,

            "total_categories": total_categories,

            "this_month_expense": this_month_expense,

            "highest_category": highest_category,

            "highest_amount": highest_amount,

            "biggest_expense": biggest_expense,

            "average_daily": average_daily,

            "last_30_total": last_30_total,

            "last_30_transactions": last_30_transactions,

            "monthly_graph": monthly_graph,

            "average_daily_expense": average_daily_expense,

            "months": months,
            "years": years,
            "month_filter": month_filter,
            "year_filter": year_filter,

        }

    )


# ==========================================
# ADD EXPENSE
# ==========================================
@login_required
def add_expense(request):

    if request.method == "POST":

        form = ExpenseForm(request.POST)

        if form.is_valid():

            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            messages.success(
                request,
                "Expense added successfully."
            )

            return redirect("home")

    else:
        form = ExpenseForm()

    return render(
        request,
        "add_expense.html",
        {
            "form": form
        }
    )
# ==========================================
# EDIT EXPENSE
# ==========================================
@login_required
def edit_expense(request, id):

    expense = get_object_or_404(
    Expense,
    id=id,
    user=request.user
    )

    if request.method == "POST":

        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Expense updated successfully."
            )

            return redirect("home")
        else:
            print(form.errors)

    else:

        form = ExpenseForm(
            instance=expense
        )

    return render(

        request,

        "add_expense.html",

        {

            "form": form

        }

    )


# ==========================================
# DELETE EXPENSE
# ==========================================
@login_required
def delete_expense(request, id):

    expense = get_object_or_404(
    Expense,
    id=id,
    user=request.user
    )

    if request.method == "POST":

        expense.delete()

        messages.success(

            request,

            "Expense deleted successfully."

        )

    return redirect("home")


# ==========================================
# CLEAR ALL EXPENSES
# ==========================================
@login_required
def clear_expenses(request):

    if request.method == "POST":

        Expense.objects.filter(user=request.user).delete()

        messages.success(

            request,

            "All expenses cleared successfully."

        )

    return redirect("home")

# ==========================================
# DOWNLOAD PDF REPORT
# ==========================================
@login_required
def download_report(request):
    search_query = request.GET.get("search", "")
    category_filter = request.GET.get("category", "")
    month_filter = request.GET.get("month", "")
    year_filter = request.GET.get("year", "")

    response = HttpResponse(content_type="application/pdf")

    filename = "Expense_Report"

    if month_filter:
        filename += f"_Month-{month_filter}"

    if year_filter:
        filename += f"_{year_filter}"

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}.pdf"'
    )

    styles = getSampleStyleSheet()

    elements = []

    # Base queryset
    expenses = Expense.objects.filter(
        user=request.user
    )
    # Search
    if search_query:
        expenses = expenses.filter(
            Q(title__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    # Category
    if category_filter:
        expenses = expenses.filter(
            category=category_filter
        )

    # Month
    if month_filter:
        expenses = expenses.filter(
            date__month=month_filter
        )

    # Year
    if year_filter:
        expenses = expenses.filter(
            date__year=year_filter
        )

    # Order
    expenses = expenses.order_by("-date", "-id")

    total = sum(
        expense.amount
        for expense in expenses
    )
    doc = SimpleDocTemplate(response)
    doc.title = "Expense Tracker Report"
    doc.author = "MD Jaheer Ashraf"
    doc.subject = "Expense Report"
    doc.creator = "Expense Tracker"

    # ==========================
    # Title
    # ==========================

    elements.append(

        Paragraph(

            "<b><font size=20>Expense Tracker Report</font></b>",

            styles["Title"]

        )

    )

    elements.append(

        Paragraph(

            f"Generated On : {datetime.now().strftime('%d-%m-%Y %I:%M %p')}",

            styles["Normal"]

        )

    )

    elements.append(Spacer(1, 15))

    elements.append(

        Paragraph(

            f"<b>Total Expense : ₹ {total}</b>",

            styles["Heading2"]

        )

    )

    elements.append(Spacer(1, 15))

    # ==========================
    # Expense Table
    # ==========================

    data = [["Title", "Amount", "Category", "Date"]]

    for expense in expenses:

        data.append([

            expense.title,

            str(expense.amount),

            expense.category,

            str(expense.date)

        ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("GRID", (0,0), (-1,-1), 1, colors.black),

            ("BACKGROUND", (0,1), (-1,-1), colors.beige),

            ("BOTTOMPADDING", (0,0), (-1,0), 10),

        ])

    )

    elements.append(table)

    elements.append(Spacer(1,25))

    # ==========================
    # Pie Chart
    # ==========================

    category_data = {}

    for expense in expenses:

        category_data[expense.category] = (

            category_data.get(expense.category, 0)

            + expense.amount

        )

    labels = list(category_data.keys())

    values = list(category_data.values())

    plt.figure(figsize=(4,4))

    if values:

        plt.pie(

            values,

            labels=labels,

            autopct="%1.1f%%"

        )

        plt.title("Expense Distribution")

    chart_buffer = BytesIO()

    plt.savefig(

        chart_buffer,

        format="png",

        bbox_inches="tight"

    )

    plt.close()

    chart_buffer.seek(0)

    elements.append(

        Paragraph(

            "<b>Expense Distribution</b>",

            styles["Heading2"]

        )

    )

    elements.append(Spacer(1,10))

    chart = Image(chart_buffer)

    chart.drawWidth = 4 * inch

    chart.drawHeight = 4 * inch

    elements.append(chart)

    elements.append(Spacer(1,20))

    elements.append(

        Paragraph(

            "<font color='grey'>Generated by Expense Tracker</font>",

            styles["Normal"]

        )

    )

    doc.build(elements)

    return response