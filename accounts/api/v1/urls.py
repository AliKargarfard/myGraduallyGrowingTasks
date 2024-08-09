from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token, ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'api-v1'

urlpatterns = [
    # Registration
    path('registration/', views.RegistrationApiView.as_view(),name='registration'),

    # Change password
    path('change-password/', views.ChangePasswordView.as_view(),name='change-password'),
    

    # Login TOKEN
    path('token/login/', views.CustomAuthToken.as_view(),name='token-sign-in'),
    path('token/logout/', views.CustomDeleteAuthToken.as_view(),name='token-sign-out'),

    #Login JWT
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(),name='jwt-create'), 
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),   
    path('jwt/verify/', TokenRefreshView.as_view(), name='jwt_verify'),

    # profile
    path('profile/', views.ProfileApiView.as_view(),name='profile'),

 ]