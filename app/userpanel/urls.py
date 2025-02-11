from django.urls import path
from .views import (
    dashboard,
    create_part,
    inventory_status,
    aircraft_list,
    assemble_aircraft,
    login_view,
    register_view,
    logout_view,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("", dashboard, name="dashboard"),
    path("create_parts/", create_part, name="create_part"),
    path("inventory_status/", inventory_status, name="inventory_status"),
    path("aircraft_list/", aircraft_list, name="aircraft_list"),
    path("assemble_aircraft/", assemble_aircraft, name="assemble_aircraft"),
]
