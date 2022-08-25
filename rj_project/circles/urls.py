from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from rj_project.circles.views import create_circles, list_circles

app_name = "circles"

from .views import circles as circle_views

router = DefaultRouter()
router.register("circles", circle_views.CircleViewSet, basename="circle")
urlpatterns = [
    path("", include(router.urls))
    # path("circles/", list_circles, name="circles"),
    # path("circles/create", create_circles, name="create"),
]
