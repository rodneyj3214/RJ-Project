from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rj_project.circles.models import Circle
from rj_project.circles.serializers import CircleSerializer, CreateCircleSerializer


@api_view(["GET"])
def list_circles(request):
    circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(circles, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_circles(request):
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle = serializer.save()
    return Response(CircleSerializer(circle).data)
