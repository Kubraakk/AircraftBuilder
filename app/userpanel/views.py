from django.shortcuts import render, redirect
from django.contrib.auth import logout, get_user_model

User = get_user_model()


def dashboard(request):
    return render(request, "userpanel/dashboard.html")


def create_part(request):
    return render(request, "userpanel/create_part.html")


def inventory_status(request):
    return render(request, "userpanel/inventory_status.html")


def aircraft_list(request):
    return render(request, "userpanel/aircraft_list.html")


def assemble_aircraft(request):
    return render(request, "userpanel/assemble_aircraft.html")


def login_view(request):
    return render(request, "userpanel/login.html")


def register_view(request):
    return render(request, "userpanel/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")
