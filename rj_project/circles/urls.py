from django.urls import path

from rj_project.circles.views import create_circles, list_circles

app_name = "circles"
urlpatterns = [
    path("circles/", list_circles, name="circles"),
    path("circles/create", create_circles, name="create"),
]
