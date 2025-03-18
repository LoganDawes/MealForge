from django.urls import path
from .views import RegisterUserView, UnregisterUserView, LoginUserView, LogoutUserView, GetPreferencesView, UpdatePreferencesView, GetRecipeInformationView, GetIngredientInformationView, GetRecipeInformationView, SearchRecipesView, SearchIngredientsView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('unregister/', UnregisterUserView.as_view(), name='unregister'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('preferences/', GetPreferencesView.as_view(), name='get_preferences'),
    path('preferences/update/', UpdatePreferencesView.as_view(), name='update_preferences'),
    path('recipes/<int:recipe_id>/', GetRecipeInformationView.as_view(), name='recipe_information'),
    path('ingredients/<int:ingredient_id>/', GetIngredientInformationView.as_view(), name='ingredient_information'),
    path('search/recipes', SearchRecipesView.as_view(), name='search_recipes'),
    path('search/ingredients', SearchIngredientsView.as_view(), name='search_ingredients'),
]