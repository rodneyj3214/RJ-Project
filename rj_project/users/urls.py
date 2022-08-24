from django.urls import path

from rj_project.users.views.users import (
    AccountVerificationAPIView,
    UserAPIView,
    UserSignupAPIView,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("login", UserAPIView.as_view(), name="login"),
    path("signup", UserSignupAPIView.as_view(), name="signup"),
    path("verify", AccountVerificationAPIView.as_view(), name="verify"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
