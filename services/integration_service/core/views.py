import requests
import json
import logging
from django.conf import settings

# REST Framework
from rest_framework.response import Response
from rest_framework.views import APIView

# CSRF Exemption
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Initialzes Logger
logger = logging.getLogger('django')

# Get Spoonacular details in settings.py
SPOONACULAR_API_KEY = settings.SPOONACULAR_API_KEY
SPOONACULAR_BASE_URL = settings.SPOONACULAR_BASE_URL

@method_decorator(csrf_exempt, name='dispatch')
class RecipeInformationView(APIView):
    def get(self, request, recipe_id):
        try:
            # LOGGER: Test received data
            logger.info(f"Recieving recipe information for recipe_id: {recipe_id}")

            # Construct API request URL
            url = f"{SPOONACULAR_BASE_URL}/recipes/{recipe_id}/information"
            params = {
                "apiKey": SPOONACULAR_API_KEY,
                "includeNutrition": 'true'
            }

            # Send get request to Spoonacular
            response = requests.get(url, params=params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Spoonacular: {response.status_code}, {response.text}")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
    
@method_decorator(csrf_exempt, name='dispatch')
class IngredientInformationView(APIView):
    def get(self, request, ingredient_id):
        try:
            # LOGGER: Test received data
            logger.info(f"Receiving ingredient information for ingredient_id: {ingredient_id}")

            logger.info(f"Full Query Params: {request.query_params}")

            # Extract optional query parameters
            amount = request.query_params.get("amount", 1)
            unit = request.query_params.get("unit", "grams")
            locale = request.query_params.get("locale", "en_US")

            logger.info(f"Extracted Params - Amount: {amount}, Unit: {unit}, Locale: {locale}")

            # Construct API request URL
            url = f"{SPOONACULAR_BASE_URL}/food/ingredients/{ingredient_id}/information"
            params = {
                "apiKey": SPOONACULAR_API_KEY,
                "amount": amount,
                "unit": unit,
                "locale": locale,
            }

            # Send get request to Spoonacular
            response = requests.get(url, params=params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Spoonacular: {response.status_code}, {response.text}")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        
@method_decorator(csrf_exempt, name='dispatch')
class SearchRecipesView(APIView):
    def get(self, request):
        try:
            # LOGGER: Test received data
            logger.info(f"Full Query Params: {request.query_params}")

            # Construct API request URL
            url = f"{SPOONACULAR_BASE_URL}/recipes/complexSearch"
            params = {
                "apiKey": SPOONACULAR_API_KEY,
            }

            # Add optional query parameters if they exist
            optional_params = [
                "query", "cuisine", "excludeCuisine", "diet", "intolerances", "equipment",
                "includeIngredients", "excludeIngredients", "type", "instructionsRequired",
                "fillIngredients", "addRecipeInformation", "addRecipeInstructions",
                "addRecipeNutrition", "author", "tags", "recipeBoxId", "titleMatch",
                "maxReadyTime", "minServings", "maxServings", "ignorePantry", "sort",
                "sortDirection", "minCarbs", "maxCarbs", "minProtein", "maxProtein",
                "minCalories", "maxCalories", "minFat", "maxFat", "minAlcohol", "maxAlcohol",
                "minCaffeine", "maxCaffeine", "minCopper", "maxCopper", "minCalcium",
                "maxCalcium", "minCholine", "maxCholine", "minCholesterol", "maxCholesterol",
                "minFluoride", "maxFluoride", "minSaturatedFat", "maxSaturatedFat",
                "minVitaminA", "maxVitaminA", "minVitaminC", "maxVitaminC", "minVitaminD",
                "maxVitaminD", "minVitaminE", "maxVitaminE", "minVitaminK", "maxVitaminK",
                "minVitaminB1", "maxVitaminB1", "minVitaminB2", "maxVitaminB2", "minVitaminB5",
                "maxVitaminB5", "minVitaminB3", "maxVitaminB3", "minVitaminB6", "maxVitaminB6",
                "minVitaminB12", "maxVitaminB12", "minFiber", "maxFiber", "minFolate",
                "maxFolate", "minFolicAcid", "maxFolicAcid", "minIodine", "maxIodine",
                "minIron", "maxIron", "minMagnesium", "maxMagnesium", "minManganese",
                "maxManganese", "minPhosphorus", "maxPhosphorus", "minPotassium", "maxPotassium",
                "minSelenium", "maxSelenium", "minSodium", "maxSodium", "minSugar", "maxSugar",
                "minZinc", "maxZinc", "offset", "number"
            ]

            # Iterate through optional query parameters
            for param in optional_params:
                value = request.query_params.get(param)
                if value is not None:
                    params[param] = value

            # Send get request to Spoonacular
            response = requests.get(url, params=params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Spoonacular: {response.status_code}, {response.text}")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        
@method_decorator(csrf_exempt, name='dispatch')
class SearchIngredientsView(APIView):
    def get(self, request):
        try:
            # LOGGER: Test received data
            logger.info(f"Full Query Params: {request.query_params}")

            # Construct API request URL
            url = f"{SPOONACULAR_BASE_URL}/food/ingredients/search"
            params = {
                "apiKey": SPOONACULAR_API_KEY,
            }

            # Add optional query parameters if they exist
            optional_params = [
                "query", "addChildren", "minProteinPercent", "maxProteinPercent", "minFatPercent",
                "maxFatPercent", "minCarbsPercent", "maxCarbsPercent", "metaInformation",
                "intolerances", "sort", "sortDirection", "language", "offset", "number"
            ]

            # Iterate through optional query parameters
            for param in optional_params:
                value = request.query_params.get(param)
                if value is not None:
                    params[param] = value

            # Set default query to 'a' if empty (required parameter)
            if 'query' not in params or not params['query']:
                params['query'] = 'a'

            # Send get request to Spoonacular
            response = requests.get(url, params=params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Spoonacular: {response.status_code}, {response.text}")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)

