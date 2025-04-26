import requests
import logging
from django.conf import settings

# REST Framework
from rest_framework.response import Response
from rest_framework.views import APIView

# Initialzes Logger
logger = logging.getLogger('django')

# Get Service's URLs in settings.py
INTEGRATION_SERVICE_URL = settings.INTEGRATION_SERVICE_URL
USER_SERVICE_URL = settings.USER_SERVICE_URL


class SearchRecipesView(APIView):
    def get(self, request):
        try:
            # LOGGER : Test received request
            logger.info(f"Received request at search_service for search")

            # Initialize query parameters
            query_params = request.query_params.copy()

            # Send get request to Integration service
            response = requests.get(f"{INTEGRATION_SERVICE_URL}/api/search/recipes/", params=query_params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Integration Service: {response.status_code} - {response.json().get('totalResults')} results")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        

class SearchIngredientsView(APIView):
    def get(self, request):
        try:
            # LOGGER : Test received request
            logger.info(f"Received request at search_service for search")

            # Initialize query parameters
            query_params = request.query_params.copy()

            # Send get request to Integration service
            response = requests.get(f"{INTEGRATION_SERVICE_URL}/api/search/ingredients/", params=query_params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Integration Service: {response.status_code} - {response.json().get('totalResults')} results")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)