from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rj_project.circles.models import Circle
from rj_project.circles.serializers.circles import CircleModelSerializer


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
