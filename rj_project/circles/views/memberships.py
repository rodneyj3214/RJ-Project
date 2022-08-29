from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from rj_project.circles.models import Circle, Membership
from rj_project.circles.permissions.memberships import IsActiveCircleMember
from rj_project.circles.serializers.memberships import MembershipModelSerializer


class MembershipViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """verify that the circle exists."""
        slug_name = kwargs["slug_name"]
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super().dispatch(request, *args, **kwargs)

    def get_permissions(self):
        permissions = [IsAuthenticated, IsActiveCircleMember]
        return (permission() for permission in permissions)

    def get_queryset(self):
        return Membership.objects.filter(circle=self.circle, is_active=True)

    def get_object(self):
        return get_object_or_404(
            Membership,
            user__username=self.kwargs["pk"],
            circle=self.circle,
            is_active=True,
        )
