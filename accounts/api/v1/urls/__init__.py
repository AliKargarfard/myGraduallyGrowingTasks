from django.urls import path, include

app_name = "ApiV1"
urlpatterns = [
    path("", include("accounts.api.v1.urls.accounts", namespace="account_urls")),
    path(
        "profile/", include("accounts.api.v1.urls.profiles", namespace="profile_urls")
    ),
]
