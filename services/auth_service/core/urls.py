from django.urls import path
from .views import RegisterView, UnregisterView, LoginView, LogoutView, RefreshTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('unregister/', UnregisterView.as_view(), name='unregister'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
]