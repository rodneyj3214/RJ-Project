from rest_framework.permissions import BasePermission

from rj_project.circles.models import Membership


class IsCircleAdmin(BasePermission):
    """Allow acces only"""

    def has_object_permission(self, request, view, obj):
        """Check object and the object are the same user"""
        try:
            Membership.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_active=True,
            )
        except Membership.DoesNotExist:
            return False
        return True
