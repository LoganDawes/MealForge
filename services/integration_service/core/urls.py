from django.urls import path
from .views import RecipeInformationView, IngredientInformationView, SearchRecipesView, SearchIngredientsView

urlpatterns = [
    path('recipes/<int:recipe_id>/', RecipeInformationView.as_view(), name='recipe_information'),
    path('ingredients/<int:ingredient_id>/', IngredientInformationView.as_view(), name='ingredient_information'),
    path('search/recipes/', SearchRecipesView.as_view(), name='search_recipes'),
    path('search/ingredients/', SearchIngredientsView.as_view(), name='search_ingredients'),
]