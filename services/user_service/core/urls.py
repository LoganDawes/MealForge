from django.urls import path
from .views import UserView, UserPreferencesView, UserRecipesView, UserIngredientsView, UpdateRecipesView, UpdateIngredientsView

urlpatterns = [
    path('users/', UserView.as_view(), name='user'),
    path("preferences/", UserPreferencesView.as_view(), name="user-preferences"),
    path("collections/recipes/", UserRecipesView.as_view(), name="user-recipes"),
    path("collections/ingredients/", UserIngredientsView.as_view(), name="user-ingredients"),
    path("collections/recipes/update/", UpdateRecipesView.as_view(), name="update-recipes"),
    path("collections/ingredients/update/", UpdateIngredientsView.as_view(), name="update-ingredients"),
]