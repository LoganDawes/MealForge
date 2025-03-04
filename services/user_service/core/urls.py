from django.urls import path, include
from .views import UserCreateView

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user-create'),
]