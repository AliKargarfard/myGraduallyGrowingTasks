from django.urls import path, include
from . import views

# from django.contrib.auth.views import LogoutView
# from .views import LoginView, RegisterView

app_name = "accounts"

urlpatterns = [
    # path("login/", LoginView.as_view(), name="login"),
    # path("logout", LogoutView.as_view(next_page="/"), name="logout"),
    # path("register/", RegisterView.as_view(), name="register"),
    path("", include("django.contrib.auth.urls")),
    path("api/v1/", include("accounts.api.v1.urls")),
    path("send-email/", views.sendEmail, name="send-email"),
    path("test/", views.test, name="send-email"),
]
