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

