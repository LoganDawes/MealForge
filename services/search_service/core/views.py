import requests
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

# Get Service's URLs in settings.py
INTEGRATION_SERVICE_URL = settings.INTEGRATION_SERVICE_URL
USER_SERVICE_URL = settings.USER_SERVICE_URL

@method_decorator(csrf_exempt, name='dispatch')
class SearchRecipesView(APIView):
    def get(self, request):
        try:
            # LOGGER : Test received request
            logger.info(f"Received request at search_service for search")

            # Initialize query parameters
            query_params = request.query_params.copy()

            # Fetch user preferences if authorization header is present
            auth_header = request.headers.get('Authorization')
            if auth_header:
                logger.info(f"Authorization header present: {auth_header}")
                try:
                    user_preferences_response = requests.get(f"{USER_SERVICE_URL}/api/preferences/", headers={"Authorization": auth_header}, timeout=10)
                    user_preferences_response.raise_for_status()
                    user_preferences = user_preferences_response.json()

                    logger.info(f"User preferences: {user_preferences}")

                    # Map user preferences to query parameters
                    if 'diets' in user_preferences:
                        query_params['diet'] = ','.join(user_preferences['diets'])
                    if 'intolerances' in user_preferences:
                        query_params['intolerances'] = ','.join(user_preferences['intolerances'])
                    if 'calorie_limit' in user_preferences:
                        query_params['maxCalories'] = user_preferences['calorie_limit']
                except requests.exceptions.RequestException as e:
                    logger.error(f"Failed to fetch user preferences: {str(e)}")
            else:
                logger.info("Authorization header not present")

            # Send get request to Integration service
            response = requests.get(f"{INTEGRATION_SERVICE_URL}/api/search/recipes/", params=query_params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Integration Service: {response.status_code}, {response.text}")

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
            # LOGGER : Test received request
            logger.info(f"Received request at search_service for search")

            # Initialize query parameters
            query_params = request.query_params.copy()

            # Fetch user preferences if authorization header is present
            auth_header = request.headers.get('Authorization')
            if auth_header:
                logger.info(f"Authorization header present: {auth_header}")
                try:
                    user_preferences_response = requests.get(f"{USER_SERVICE_URL}/api/preferences/", headers={"Authorization": auth_header}, timeout=10)
                    user_preferences_response.raise_for_status()
                    user_preferences = user_preferences_response.json()

                    logger.info(f"User preferences: {user_preferences}")

                    # Map user preferences to query parameters
                    if 'intolerances' in user_preferences:
                        query_params['intolerances'] = ','.join(user_preferences['intolerances'])
                    else:
                        logger.info("Intolerances not present in user preferences")
                except requests.exceptions.RequestException as e:
                    logger.error(f"Failed to fetch user preferences: {str(e)}")
            else:
                logger.info("Authorization header not present")

            # Send get request to Integration service
            response = requests.get(f"{INTEGRATION_SERVICE_URL}/api/search/ingredients/", params=query_params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Integration Service: {response.status_code}, {response.text}")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)