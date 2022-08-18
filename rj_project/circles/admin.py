from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Models
from rj_project.circles.models import Circle
from rj_project.users.forms import UserAdminChangeForm, UserAdminCreationForm


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display = [
        "slug_name",
        "name",
        "is_public",
        "verified",
        "is_limited",
        "members_limit",
    ]

    search_fields = ["slug_name", "name"]
    list_filter = ("is_public", "verified", "is_limited")
