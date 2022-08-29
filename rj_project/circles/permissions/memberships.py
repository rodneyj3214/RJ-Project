from rest_framework.permissions import BasePermission

from rj_project.circles.models import Membership


class IsActiveCircleMember(BasePermission):
    def has_permission(self, request, view):
        try:
            Membership.objects.get(
                user=request.user, circle=view.circle, is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True
