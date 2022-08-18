from django.db import models
from django.utils.translation import gettext_lazy as _

from rj_project.utils.models import CRideModel


class Profile(CRideModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)

    picture = models.ImageField(_("Profile picture"))
    biography = models.TextField(max_length=500, blank=True)

    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)
    reputation = models.FloatField(
        default=5.0,
        help_text=_("User's reputation based on the rides taken and offered."),
    )

    def __str__(self):
        """Return User's str representation"""
        return str(self.user)
