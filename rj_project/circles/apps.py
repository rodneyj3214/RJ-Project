from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CirclesConfig(AppConfig):
    name = "rj_project.circles"
    verbose_name = _("Circles")

    def ready(self):
        try:
            import rj_project.users.signals  # noqa F401
        except ImportError:
            pass
