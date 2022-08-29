from rest_framework import serializers

from rj_project.circles.models import Membership
from rj_project.users.serializers.users import UserModelSerializer


class MembershipModelSerializer(serializers.ModelSerializer):
    """Member model serializer"""

    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source="created", read_only=True)

    class Meta:
        model = Membership
        fields = (
            "user",
            "is_admin",
            "is_active",
            "used_invitations",
            "remaining_invitations",
            "invited_by",
            "rides_taken",
            "rides_offered",
            "joined_at",
        )
        read_only_fields = (
            "user",
            "used_invitations",
            "invited_by",
            "rides_taken",
            "rides_offered",
        )
