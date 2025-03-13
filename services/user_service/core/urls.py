from django.urls import path
from .views import UserView, UserPreferencesView

urlpatterns = [
    path('users/', UserView.as_view(), name='user'),
    path("preferences/", UserPreferencesView.as_view(), name="user-preferences"),
]