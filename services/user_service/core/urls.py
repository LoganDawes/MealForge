from django.urls import path, include
from .views import UserView, AuthenticateUserView, LogoutUserView, UserPreferencesView

urlpatterns = [
    path('users/', UserView.as_view(), name='user'),
    path('authenticate/', AuthenticateUserView.as_view(), name='authenticate'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path("preferences/", UserPreferencesView.as_view(), name="user-preferences"),
]