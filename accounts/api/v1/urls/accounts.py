from django.urls import path
from .. import views

# from rest_framework.authtoken.views import obtain_auth_token, ObtainAuthToken
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "account_urls"

urlpatterns = [
    # Registration
    path("register/", views.RegisterApiView.as_view(), name="register"),
    # path('email-test/', views.EmailTestView.as_view(),name='email-test'),
    # Change password
    path("change-password", views.ChangePasswordView.as_view(), name="change-password"),
    # activation
    path(
        "activation/confirm/<str:token>",
        views.ActivationApiView.as_view(),
        name="activation",
    ),
    # resend activation
    path(
        "activation/resend",
        views.ActivationResendApiView.as_view(),
        name="activation-resend",
    ),
    # Login TOKEN
    path("token/login/", views.CustomAuthToken.as_view(), name="token-sign-in"),
    path("token/logout/", views.CustomDeleteAuthToken.as_view(), name="token-sign-out"),
    # Login JWT
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
