from django.urls import path
from .views import UserView, UserPreferencesView, UserRecipesView, UserIngredientsView

urlpatterns = [
    path('users/', UserView.as_view(), name='user'),
    path("preferences/", UserPreferencesView.as_view(), name="user-preferences"),
    path("collections/recipes/", UserRecipesView.as_view(), name="user-recipes"),
    path("collections/ingredients/", UserIngredientsView.as_view(), name="user-ingredients")
]