from django.contrib import admin

from .models import User


# Register admin for Receiver model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Registering User in Admin"""

    list_display = ("id", "email", "password")
