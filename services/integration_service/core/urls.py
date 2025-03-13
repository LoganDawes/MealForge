from django.urls import path
from .views import RecipeInformationView, IngredientInformationView

urlpatterns = [
    path('recipes/<int:recipe_id>/', RecipeInformationView.as_view(), name='recipe_information'),
    path('ingredients/<int:ingredient_id>/', IngredientInformationView.as_view(), name='ingredient_information'),
]