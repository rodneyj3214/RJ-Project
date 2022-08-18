from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rj_project.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
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
    list_display = [
        "email",
        "username",
        "name",
        "is_staff",
        "is_client",
        "is_superuser",
    ]
    filter = ("is_client", "is_staff", "created", "modified")
    search_fields = ["name"]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "reputation", "rides_taken", "rides_offered")
    search_fields = (
        "user__username",
        "user__email",
        "reputation",
        "rides_taken",
        "rides_offered",
    )
    list_filter = ("reputation",)
