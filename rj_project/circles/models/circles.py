from django.db import models

from rj_project.utils.models import CRideModel


class Circle(CRideModel):
    name = models.CharField("Circle Name", max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)

    about = models.CharField("Circle description", max_length=255)
    picture = models.ImageField(upload_to="circles/pictures", blank=True, null=True)

    members = models.ManyToManyField(
        "users.User",
        through="circles.Membership",
        through_fields=("circle", "user"),
        related_name="members",
    )
    # stats
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(
        default=False,
        help_text="Verified circles are also known as official communities.",
    )
    is_public = models.BooleanField(
        default=False,
        help_text="Public circles are listed in the main page so everyone know about their existence.",
    )
    is_limited = models.BooleanField(default=False)
    members_limit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta(CRideModel.Meta):
        ordering = ["-rides_taken", "-rides_offered"]
