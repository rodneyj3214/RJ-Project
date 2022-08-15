from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import BooleanField, CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Utilities
from rj_project.utils.models import CRideModel


class User(CRideModel, AbstractUser):
    """
    Default custom user model for RJ Project.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    email = EmailField(
        _("Email address"),
        unique=True,
        error_messages={"unique": "A user with that email already exists."},
    )

    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be in the format: +9999999. Up 15 digits allowed.",
    )
    phone_number = CharField(max_length=17, validators=[phone_regex], blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    is_client = BooleanField(
        "client status",
        default=True,
        help_text=(
            "Help easily distinguish users and perform queries."
            "Clients are the main of user"
        ),
    )
    is_verified = BooleanField(
        "verified", default=False, help_text="Verified users for new test"
    )
    name = CharField("Name", max_length=75, blank=True)

    def __str__(self):
        return self.username

    def get_short_name(self) -> str:
        return self.username

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
