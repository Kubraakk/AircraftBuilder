from django.contrib import admin
from apps.part.models import Part, Inventory, Assembly, AssemblyPartUsage


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "aircraft", "team")
    list_filter = ("aircraft", "team")
    search_fields = ("name", "aircraft__aircraft_name")
    ordering = ("aircraft", "name")


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("id", "part", "quantity")
    list_filter = ("part__aircraft",)
    search_fields = ("part__name", "part__aircraft__aircraft_name")
    ordering = ("part__aircraft", "part__name")


@admin.register(Assembly)
class AssemblyAdmin(admin.ModelAdmin):
    list_display = ("id", "aircraft", "created_at")
    ordering = ("-created_at",)
    search_fields = ("aircraft__aircraft_name",)
    filter_horizontal = ("parts_used",)


@admin.register(AssemblyPartUsage)
class AssemblyPartUsageAdmin(admin.ModelAdmin):
    list_display = ("id", "assembly", "part", "quantity_used")
    list_filter = ("assembly__aircraft", "part__name")
    ordering = ("assembly__aircraft", "part__name")
