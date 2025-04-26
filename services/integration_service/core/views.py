import requests
import logging
from django.conf import settings
from django.core.cache import cache

# REST Framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Initialzes Logger
logger = logging.getLogger('django')

# Get Spoonacular details in settings.py
SPOONACULAR_API_KEY = settings.SPOONACULAR_API_KEY
SPOONACULAR_BASE_URL = settings.SPOONACULAR_BASE_URL

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

            # Generate cache key based on recipe_id and query parameters
            cache_key = f"recipe_information_{recipe_id}_{hash(frozenset(params.items()))}"

            # Check if response is cached
            cached_response = cache.get(cache_key)
            if cached_response:
                logger.info("Returning cached response")
                return Response(cached_response, status=status.HTTP_200_OK)

            # Send get request to Spoonacular
            response = requests.get(url, params=params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # Cache the response
            cache.set(cache_key, response.json(), timeout=settings.SPOONACULAR_CACHE_TIMEOUT)

            # LOGGER: Test response data
            logger.info(f"Response from Spoonacular: {response.status_code} - {response.json().get('title')}")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
    

class IngredientInformationView(APIView):
    def get(self, request, ingredient_id):
        try:
            # LOGGER: Test received data
            logger.info(f"Receiving ingredient information for ingredient_id: {ingredient_id}")

            # Extract optional query parameters
            amount = request.query_params.get("amount", 1)
            unit = request.query_params.get("unit", "grams")
            locale = request.query_params.get("locale", "en_US")

            # Construct API request URL
            url = f"{SPOONACULAR_BASE_URL}/food/ingredients/{ingredient_id}/information"
            params = {
                "apiKey": SPOONACULAR_API_KEY,
                "amount": amount,
                "unit": unit,
                "locale": locale,
            }

            # Generate cache key based on ingredient_id and query parameters
            cache_key = f"ingredient_information_{ingredient_id}_{hash(frozenset(params.items()))}"

            # Check if response is cached
            cached_response = cache.get(cache_key)
            if cached_response:
                logger.info("Returning cached response")
                return Response(cached_response, status=status.HTTP_200_OK)

            # Send get request to Spoonacular
            response = requests.get(url, params=params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # Cache the response
            cache.set(cache_key, response.json(), timeout=settings.SPOONACULAR_CACHE_TIMEOUT)

            # LOGGER: Test response data
            logger.info(f"Response from Spoonacular: {response.status_code} - {response.json().get('name')}")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        

class SearchRecipesView(APIView):
    def get(self, request):
        try:
            # DEBUG
            logger.info(f"Received Query Params: {request.query_params}")
            
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
                    
            # Generate cache key based on query parameters
            cache_key = f"search_recipes_{hash(frozenset(params.items()))}"

            # Check if response is cached
            cached_response = cache.get(cache_key)
            if cached_response:
                logger.info("Returning cached response")
                return Response(cached_response, status=status.HTTP_200_OK)

            # Send get request to Spoonacular
            response = requests.get(url, params=params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # Cache the response
            cache.set(cache_key, response.json(), timeout=settings.SPOONACULAR_CACHE_TIMEOUT)

            # LOGGER: Test response data
            logger.info(f"Response from Spoonacular: {response.status_code} - {response.json().get('totalResults')} results")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        

class SearchIngredientsView(APIView):
    def get(self, request):
        try:
            # DEBUG
            logger.info(f"Received Query Params: {request.query_params}")
            
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
                
            # Generate cache key based on query parameters
            cache_key = f"search_ingredients_{hash(frozenset(params.items()))}"

            # Check if response is cached
            cached_response = cache.get(cache_key)
            if cached_response:
                logger.info("Returning cached response")
                return Response(cached_response, status=status.HTTP_200_OK)

            # Send get request to Spoonacular
            response = requests.get(url, params=params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # Cache the response
            cache.set(cache_key, response.json(), timeout=settings.SPOONACULAR_CACHE_TIMEOUT)

            # LOGGER: Test response data
            logger.info(f"Response from Spoonacular: {response.status_code} - {response.json().get('totalResults')} results")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)

