from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm,CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "first_name", "last_name", "email", "avatar", ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("avatar", )}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("avatar", )}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
