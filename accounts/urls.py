from django.urls import path

from . import views


urlpatterns = [
    path("<int:pk>/", views.UserUpdate.as_view(), name="profile")
]
