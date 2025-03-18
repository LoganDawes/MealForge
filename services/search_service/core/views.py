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

# Get Service's URLs in settings.py
INTEGRATION_SERVICE_URL = settings.INTEGRATION_SERVICE_URL

@method_decorator(csrf_exempt, name='dispatch')
class SearchRecipesView(APIView):
    def get(self, request):
        try:
            # LOGGER : Test received request
            logger.info(f"Received request at search_service for search")

            # Send get request to Integration service
            response = requests.get(f"{INTEGRATION_SERVICE_URL}/api/search/recipes/", params=request.query_params, headers= {"Content-Type": "application/json"}, timeout=10)
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

            # Send get request to Integration service
            response = requests.get(f"{INTEGRATION_SERVICE_URL}/api/search/ingredients/", params=request.query_params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Integration Service: {response.status_code}, {response.text}")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)