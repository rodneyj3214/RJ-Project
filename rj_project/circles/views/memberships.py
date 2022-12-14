from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rj_project.circles.models import Circle, Invitation, Membership
from rj_project.circles.permissions.memberships import (
    IsActiveCircleMember,
    IsSelfMember,
)
from rj_project.circles.serializers.memberships import (
    AddMemberSerializer,
    MembershipModelSerializer,
)


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
        permissions = [IsAuthenticated]
        if self.action != "create":
            permissions.append(IsActiveCircleMember)
        if self.action == "invitations":
            permissions.append(IsSelfMember)

        return [permission() for permission in permissions]

    def get_queryset(self):
        return Membership.objects.filter(circle=self.circle, is_active=True)

    def get_object(self):
        return get_object_or_404(
            Membership,
            user__username=self.kwargs["pk"],
            circle=self.circle,
            is_active=True,
        )

    def perform_destroy(self, instance):
        instance.is_active = True
        instance.save()

    @action(detail=True, methods=["get"])
    def invitations(self, request, *args, **kwargs):
        member = self.get_object()
        invited_members = Membership.objects.filter(
            circle=self.circle, invited_by=request.user, is_active=True
        )
        unused_invitation = Invitation.objects.filter(
            circle=self.circle, issued_by=request.user, used=False
        ).values_list("code")
        diff = member.remaining_invitations - len(unused_invitation)
        invitations = [x[0] for x in unused_invitation]
        for i in range(0, diff):
            invitations.append(
                Invitation.objects.create(
                    issued_by=request.user, circle=self.circle
                ).code
            )
        data = {
            "invitations": invitations,
            "used_invitations": MembershipModelSerializer(
                invited_members, many=True
            ).data,
        }
        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = AddMemberSerializer(
            data=request.data, context={"circle": self.circle, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        data = self.get_serializer(member).data
        return Response(data, status=status.HTTP_201_CREATED)
