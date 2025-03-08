from django.urls import path, include
from .views import UserView
from .views import AuthenticateUserView
from .views import LogoutUserView

urlpatterns = [
    path('users/', UserView.as_view(), name='user'),
    path('authenticate/', AuthenticateUserView.as_view(), name='authenticate'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]