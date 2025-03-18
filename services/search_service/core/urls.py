from django.urls import path
from .views import SearchRecipesView, SearchIngredientsView

urlpatterns = [
    path('search/recipes/', SearchRecipesView.as_view(), name='search_recipes'),
    path('search/ingredients/', SearchIngredientsView.as_view(), name='search_ingredients'),
]