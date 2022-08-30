from rest_framework.permissions import BasePermission

from rj_project.circles.models import Membership


class IsActiveCircleMember(BasePermission):
    def has_permission(self, request, view):
        try:
            Membership.objects.filter(
                user=request.user, circle=view.circle, is_active=True
            ).first()
        except Membership.DoesNotExist:
            return False
        return True


class IsSelfMember(BasePermission):
    """Allow access only to the owner of the invitations."""

    def has_permission(self, request, view):
        """Check object and user"""

        obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
