from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm

from expenses.models import Expense


# =====================================
# Register
# =====================================

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "🎉 Account created successfully!"
            )

            return redirect("home")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


# =====================================
# Login
# =====================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            messages.success(
                request,
                "✅ Login Successful!"
            )

            return redirect("home")

        else:

            messages.error(
                request,
                "❌ Invalid Username or Password"
            )

    return render(
        request,
        "accounts/login.html"
    )


# =====================================
# Logout
# =====================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "👋 Logged out successfully."
    )

    return redirect("login")


# =====================================
# Profile
# =====================================

@login_required
def profile(request):

    expenses = Expense.objects.filter(
        user=request.user
    )

    total = sum(
        expense.amount
        for expense in expenses
    )

    context = {

        "total_expense": total,

        "total_transactions": expenses.count(),

        "user": request.user,

    }

    return render(
        request,
        "accounts/profile.html",
        context
    )