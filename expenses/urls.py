from django.urls import path
from . import views

urlpatterns = [

    # ==========================================
    # Home Page
    # ==========================================

    path(
        '',
        views.home,
        name='home'
    ),

    # ==========================================
    # Add Expense
    # ==========================================

    path(
        'add/',
        views.add_expense,
        name='add_expense'
    ),

    # ==========================================
    # Edit Expense
    # ==========================================

    path(
        'edit/<int:id>/',
        views.edit_expense,
        name='edit_expense'
    ),

    # ==========================================
    # Delete Expense
    # ==========================================

    path(
        'delete/<int:id>/',
        views.delete_expense,
        name='delete_expense'
    ),

    # ==========================================
    # Clear All Expenses
    # ==========================================

    path(
        'clear/',
        views.clear_expenses,
        name='clear_expenses'
    ),

    # ==========================================
    # Download PDF Report
    # ==========================================

    path(
        'download/',
        views.download_report,
        name='download_report'
    ),

]