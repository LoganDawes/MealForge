from django.urls import path, include
from .views import RegisterUserView, UnregisterUserView, LoginUserView, LogoutUserView, GetPreferencesView, UpdatePreferencesView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('unregister/', UnregisterUserView.as_view(), name='unregister'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('preferences/', GetPreferencesView.as_view(), name='get_preferences'),
    path('preferences/update/', UpdatePreferencesView.as_view(), name='update_preferences'),

]