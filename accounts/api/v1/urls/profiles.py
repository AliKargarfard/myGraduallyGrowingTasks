from django.urls import path, include
from .. import views

app_name = 'profile_urls'

urlpatterns = [
    # profile
    path("profile/", views.ProfileApiView.as_view(), name="profile"),
]
