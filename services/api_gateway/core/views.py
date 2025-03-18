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
AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL
USER_SERVICE_URL = settings.USER_SERVICE_URL
INTEGRATION_SERVICE_URL = settings.INTEGRATION_SERVICE_URL
SEARCH_SERVICE_URL = settings.SEARCH_SERVICE_URL

@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(APIView):
    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER : Test received data
            logger.info(f"Received Data at api_gateway for register: {data}")

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/api/register/", json=data, headers={"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            logger.info(f"Response from Auth Service: {response.status_code}, {response.text}")

            # Return response from Auth service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        
@method_decorator(csrf_exempt, name='dispatch')
class UnregisterUserView(APIView):
    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER : Test received data
            logger.info(f"Received Data at api_gateway for unregister: {data}")

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/api/unregister/", json=data, headers={"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            logger.info(f"Response from Auth Service: {response.status_code}, {response.text}")

            # Return response from Auth service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
    
@method_decorator(csrf_exempt, name='dispatch')
class LoginUserView(APIView):
    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER: Test received data
            logger.info(f"Received Data at api_gateway for login: {data}")

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/api/login/", json=data, headers={"Content-Type": "application/json"}, timeout=10)
            logger.info(f"Response from Auth Service: {response.status_code}, {response.text}")

            # Return response from Auth Service
            return Response(response.json(), status=response.status_code)

        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for login")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
    
@method_decorator(csrf_exempt, name='dispatch')
class LogoutUserView(APIView):
    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER: Test received data
            logger.info(f"Received Data at api_gateway for logout: {data}")

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/api/logout/", json=data, headers={"Content-Type": "application/json"}, timeout=10)
            logger.info(f"Response from Auth Service: {response.status_code}, {response.text}")

            # LOGGER : Test response data
            logger.info(f"Response from Auth Service: {response.status_code}, {response.text}")

            # Return response from Auth Service
            return Response(response.json(), status=response.status_code)

        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for logout")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        
@method_decorator(csrf_exempt, name='dispatch')
class RefreshTokenView(APIView):
    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER: Test received data
            logger.info(f"Received Data at api_gateway for refresh token: {data}")

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/api/refresh_token/", json=data, headers={"Content-Type": "application/json"}, timeout=10)
            logger.info(f"Response from Auth Service: {response.status_code}, {response.text}")

            # LOGGER : Test response data
            logger.info(f"Response from Auth Service: {response.status_code}, {response.text}")

            # Return response from Auth Service
            return Response(response.json(), status=response.status_code)

        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for refresh token")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        
@method_decorator(csrf_exempt, name='dispatch')
class GetPreferencesView(APIView):
    def get(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.info(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]

            # LOGGER: Test received token
            logger.info(f"Received Token for Get Preferences: {token}")

            # Send get request to User service
            response = requests.get(f"{USER_SERVICE_URL}/api/preferences/", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            logger.info(f"Response from User Service: {response.status_code}, {response.text}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class UpdatePreferencesView(APIView):
    def put(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.info(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]
            
            # LOGGER: Test received token
            logger.info(f"Received Token for Update Preferences: {token}")

            # Read JSON
            data = json.loads(request.body)

            # LOGGER: Test received data
            logger.info(f"Sending Data to User Service for update preferences: {data}")

            # Send put request to User service
            response = requests.put(f"{USER_SERVICE_URL}/api/preferences/", json=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            logger.info(f"Response from User Service: {response.status_code}, {response.text}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        
@method_decorator(csrf_exempt, name='dispatch')
class GetRecipeInformationView(APIView):
    def get(self, request, recipe_id):
        try:
            # LOGGER: Test received data
            logger.info(f"Recieving recipe information for recipe_id: {recipe_id}")

            # Send get request to Integration service
            response = requests.get(f"{INTEGRATION_SERVICE_URL}/api/recipes/{recipe_id}/", headers= {"Content-Type": "application/json"}, timeout=10)
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
class GetIngredientInformationView(APIView):
    def get(self, request, ingredient_id):
        try:
            # LOGGER: Test received data
            logger.info(f"Recieving ingredient information for ingredient_id: {ingredient_id}")

            logger.info(f"Full Query Params: {request.query_params}")

            # Send get request to Integration service
            response = requests.get(f"{INTEGRATION_SERVICE_URL}/api/ingredients/{ingredient_id}/", params=request.query_params, headers= {"Content-Type": "application/json"}, timeout=10)
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
class SearchRecipesView(APIView):
    def get(self, request):
        try:
            # LOGGER: Test received data
            logger.info(f"Received request at api_gateway for search")

            # Send get request to Search service
            response = requests.get(f"{SEARCH_SERVICE_URL}/api/search/recipes/", params=request.query_params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Search Service: {response.status_code}, {response.text}")

            # Return response from Search service
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
            logger.info(f"Received request at api_gateway for search")

            # Send get request to Search service
            response = requests.get(f"{SEARCH_SERVICE_URL}/api/search/ingredients/", params=request.query_params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Search Service: {response.status_code}, {response.text}")

            # Return response from Search service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
