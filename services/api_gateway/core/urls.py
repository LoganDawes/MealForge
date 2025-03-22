from django.urls import path
from .views import RegisterUserView, UnregisterUserView, LoginUserView, LogoutUserView, GetPreferencesView, UpdatePreferencesView, GetRecipeInformationView, GetIngredientInformationView, SearchRecipesView, SearchIngredientsView, RefreshTokenView, UserRecipesView, UserIngredientsView, UpdateUserRecipesView, UpdateUserIngredientsView

urlpatterns = [
    # Basic User Registration and Authentication
    path('register/', RegisterUserView.as_view(), name='register'),
    path('unregister/', UnregisterUserView.as_view(), name='unregister'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),

    # User Preferences
    path('preferences/', GetPreferencesView.as_view(), name='get_preferences'),
    path('preferences/update/', UpdatePreferencesView.as_view(), name='update_preferences'),

    # Recipe and Ingredient Information
    path('recipes/<int:recipe_id>/', GetRecipeInformationView.as_view(), name='recipe_information'),
    path('ingredients/<int:ingredient_id>/', GetIngredientInformationView.as_view(), name='ingredient_information'),

    # Search Recipes and Ingredients
    path('search/recipes', SearchRecipesView.as_view(), name='search_recipes'),
    path('search/ingredients', SearchIngredientsView.as_view(), name='search_ingredients'),

    # User Recipes and Ingredients
    path('user/recipes/', UserRecipesView.as_view(), name='user_recipes'),
    path('user/ingredients/', UserIngredientsView.as_view(), name='user_ingredients'),

    # Update User Recipes and Ingredients
    path('user/recipes/update/', UpdateUserRecipesView.as_view(), name='update_user_recipes'),
    path('user/ingredients/update/', UpdateUserIngredientsView.as_view(), name='update_user_ingredients'),
    
]