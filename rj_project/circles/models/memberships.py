from django.db import models

from rj_project.utils.models import CRideModel


class Membership(CRideModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    circle = models.ForeignKey("circles.Circle", on_delete=models.CASCADE)

    is_admin = models.BooleanField(
        "Circle Admin",
        default=False,
        help_text="Circle admins can update circle's data and manage its members",
    )

    used_invitations = models.PositiveSmallIntegerField(default=0)
    remaining_invitations = models.PositiveSmallIntegerField(default=0)
    invited_by = models.ForeignKey(
        "users.User", null=True, on_delete=models.SET_NULL, related_name="invited_by"
    )
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(
        "Active Status", default=True, help_text="Only active users ar allowed"
    )

    def __str__(self):
        return f"@{self.user.username} at #{self.circle.slug_name}"
