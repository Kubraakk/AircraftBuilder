from django.contrib import admin
from apps.aircraft.models import Aircraft


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ("id", "aircraft_name", "get_aircraft_name_display")
    search_fields = ("aircraft_name",)
    list_filter = ("aircraft_name",)
