from django.contrib import admin
from apps.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("uuid", "first_name", "last_name", "email", "team")
    search_fields = ("first_name", "team")
    list_filter = ("team",)
