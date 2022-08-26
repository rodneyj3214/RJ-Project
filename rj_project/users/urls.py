from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rj_project.users.views import users as user_views
from rj_project.users.views.users import (  # AccountVerificationAPIView,; UserAPIView,; UserSignupAPIView,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"

router = DefaultRouter()
router.register(r"", user_views.UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    # path("login", UserAPIView.as_view(), name="login"),
    # path("signup", UserSignupAPIView.as_view(), name="signup"),
    # path("verify", AccountVerificationAPIView.as_view(), name="verify"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
