from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("username", "email", "is_staff", "is_active", "is_superuser")
    list_filter = ("email", "is_staff", "is_active", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "full_name",
                    "phone",
                    "address",
                    "city",
                    "state",
                    "zip_code",
                    "nic_number",
                    "gender",
                    "user_type",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "full_name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "phone",
                    "address",
                    "city",
                    "state",
                    "zip_code",
                    "nic_number",
                    "gender",
                    "user_type",
                ),
            },
        ),
    )
    ordering = ("username",)


admin.site.register(User, UserAdmin)
