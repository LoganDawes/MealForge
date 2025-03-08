from django.urls import path, include
from .views import RegisterUserView
from .views import UnregisterUserView
from .views import LoginUserView
from .views import LogoutUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('unregister/', UnregisterUserView.as_view(), name='unregister'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]