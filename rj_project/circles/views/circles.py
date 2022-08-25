from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rj_project.circles.models import Circle, Membership
from rj_project.circles.serializers.circles import CircleModelSerializer
from rj_project.users.models import Profile


class CircleViewSet(viewsets.ModelViewSet):
    """Circle Viewset"""

    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Circle.objects.all()
        if self.action == "list":
            queryset = queryset.filter(is_public=True)
        return queryset

    def perform_create(self, serializer):
        circle = serializer.save()
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10,
        )
