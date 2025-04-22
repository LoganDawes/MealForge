import requests
import logging
from django.conf import settings

# REST Framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError

# Initialzes Logger
logger = logging.getLogger('django')

# Get Service's URLs in settings.py
AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL
USER_SERVICE_URL = settings.USER_SERVICE_URL
INTEGRATION_SERVICE_URL = settings.INTEGRATION_SERVICE_URL
SEARCH_SERVICE_URL = settings.SEARCH_SERVICE_URL

class RegisterUserView(APIView):
    def post(self, request):
        try:
            # Read JSON
            data = request.data

            # LOGGER : Test received data
            logger.info(f"Received Data at api_gateway for register")

            # Send post request to Auth service
            response = requests.post(
                f"{AUTH_SERVICE_URL}/api/register/",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            # LOGGER : Test response data
            logger.info(f"Response from Auth Service: {response.status_code} - {response.text}")

            # Return response from Auth service
            return Response(response.json(), status=response.status_code)

        # Exception Handling
        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors and forward the error response
            logger.error(f"HTTPError: {e.response.status_code} - {e.response.text}")
            return Response(e.response.json(), status=e.response.status_code)

        except ParseError:
            logger.error("Invalid JSON data received")
            return Response({"message": "Invalid JSON data"}, status=400)

        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        

class UnregisterUserView(APIView):
    def post(self, request):
        try:
            # Read JSON
            data = request.data

            # LOGGER : Test received data
            logger.info(f"Received Data at api_gateway for unregister")

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/api/unregister/", json=data, headers={"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            logger.info(f"Response from Auth Service: {response.status_code} - {response.text}")

            # Return response from Auth service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except ParseError:
            logger.error("Invalid JSON data received")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
    

class LoginUserView(APIView):
    def post(self, request):
        try:
            # Read JSON
            data = request.data

            # LOGGER: Test received data
            logger.info(f"Received Data at api_gateway for login")

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/api/login/", json=data, headers={"Content-Type": "application/json"}, timeout=10)
            logger.info(f"Response from Auth Service: {response.status_code} - {response.json().get('message')}")

            # Return response from Auth Service
            return Response(response.json(), status=response.status_code)

        # Exception Handling
        except ParseError:
            logger.error("Invalid JSON data received for login")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
    

class LogoutUserView(APIView):
    def post(self, request):
        try:
            # Read JSON
            data = request.data

            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.error(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]

            # LOGGER: Test received data
            logger.info(f"Received Data at api_gateway for logout")

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/api/logout/", json=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)

            # LOGGER : Test response data
            logger.info(f"Response from Auth Service: {response.status_code} - {response.text}")

            # Return response from Auth Service
            return Response(response.json(), status=response.status_code)

        # Exception Handling
        except ParseError:
            logger.error("Invalid JSON data received for logout")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        

class RefreshTokenView(APIView):
    def post(self, request):
        try:
            # Read JSON
            data = request.data

            # LOGGER: Test received data
            logger.info(f"Received Data at api_gateway for refresh token")

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/api/refresh_token/", json=data, headers={"Content-Type": "application/json"}, timeout=10)

            # LOGGER : Test response data
            logger.info(f"Response from Auth Service: {response.status_code} - {response.json().get('message')}")

            # Return response from Auth Service
            return Response(response.json(), status=response.status_code)

        # Exception Handling
        except ParseError:
            logger.error("Invalid JSON data received for refresh token")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        

class GetPreferencesView(APIView):
    def get(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.error(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]

            # LOGGER: Test received token
            logger.info(f"Received Token for Get Preferences")

            # Send get request to User service
            response = requests.get(f"{USER_SERVICE_URL}/api/preferences/", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            logger.info(f"Response from User Service: {response.status_code} - {response.text}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)


class UpdatePreferencesView(APIView):
    def put(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.error(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]
            
            # LOGGER: Test received token
            logger.info(f"Received Token for Update Preferences")

            # Read JSON
            data = request.data

            # LOGGER: Test received data
            logger.info(f"Sending Data to User Service for update preferences")

            # Send put request to User service
            response = requests.put(f"{USER_SERVICE_URL}/api/preferences/", json=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            logger.info(f"Response from User Service: {response.status_code} - {response.text}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except ParseError:
            logger.error("Invalid JSON data received for update preferences")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        

class GetRecipeInformationView(APIView):
    def get(self, request, recipe_id):
        try:
            # LOGGER: Test received data
            logger.info(f"Recieving recipe information for recipe_id: {recipe_id}")

            # Send get request to Integration service
            response = requests.get(f"{INTEGRATION_SERVICE_URL}/api/recipes/{recipe_id}/", headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Integration Service: {response.status_code} - {response.json().get('title')}")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        

class GetIngredientInformationView(APIView):
    def get(self, request, ingredient_id):
        try:
            # LOGGER: Test received data
            logger.info(f"Recieving ingredient information for ingredient_id: {ingredient_id}")

            # Send get request to Integration service
            response = requests.get(f"{INTEGRATION_SERVICE_URL}/api/ingredients/{ingredient_id}/", params=request.query_params, headers= {"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Integration Service: {response.status_code} - {response.json().get('name')}")

            # Return response from Integration service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        

class SearchRecipesView(APIView):
    def get(self, request):
        try:
            # LOGGER: Test received data
            logger.info(f"Received request at api_gateway for recipe search")

            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.info(f"Authorization header missing")
            else:
                # Access Token
                auth_parts = auth_header.split(" ")
                if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                    logger.error("Invalid Authorization header format")
                token = auth_parts[1]

            headers = {"Content-Type": "application/json"}
            if auth_header:
                headers["Authorization"] = f"Bearer {token}"

            # Send get request to Search service
            response = requests.get(f"{SEARCH_SERVICE_URL}/api/search/recipes/", params=request.query_params, headers=headers, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Search Service: {response.status_code} - {response.json().get('totalResults')} results")

            # Return response from Search service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        

class SearchIngredientsView(APIView):
    def get(self, request):
        try:
            # LOGGER: Test received data
            logger.info(f"Received request at api_gateway for ingredient search")

            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.info(f"Authorization header missing")
            else:
                # Access Token
                auth_parts = auth_header.split(" ")
                if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                    logger.error("Invalid Authorization header format")
                token = auth_parts[1]

            headers = {"Content-Type": "application/json"}
            if auth_header:
                headers["Authorization"] = f"Bearer {token}"

            # Send get request to Search service
            response = requests.get(f"{SEARCH_SERVICE_URL}/api/search/ingredients/", params=request.query_params, headers=headers, timeout=10)
            response.raise_for_status()

            # LOGGER: Test response data
            logger.info(f"Response from Search Service: {response.status_code} - {response.json().get('totalResults')} results")

            # Return response from Search service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)


class UserRecipesView(APIView):
    # GET request
    def get(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.error(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]

            # LOGGER: Test received token
            logger.info(f"Received Token for Get User Recipes")

            # Send get request to User service
            response = requests.get(f"{USER_SERVICE_URL}/api/collections/recipes/", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            recipes = response.json().get('recipes', [])
            titles = [recipe.get('title') for recipe in recipes]
            logger.info(f"Response from User Service: {response.status_code} - {titles}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        
    # POST request
    def post(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.error(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]

            # LOGGER: Test received token
            logger.info(f"Received Token for Add User Recipes")

            # Read JSON
            data = request.data

            # LOGGER: Test received data
            logger.info(f"Sending Data to User Service for add recipes")

            # Send post request to User service
            response = requests.post(f"{USER_SERVICE_URL}/api/collections/recipes/", json=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            recipes = response.json().get('recipes', [])
            titles = [recipe.get('title') for recipe in recipes]
            logger.info(f"Response from User Service: {response.status_code} - {titles}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except ParseError:
            logger.error("Invalid JSON data received for add user recipes")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        
    # DELETE request
    def delete(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.error(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]

            # LOGGER: Test received token
            logger.info(f"Received Token for Remove User Recipes")

            # Read JSON
            data = request.data

            # LOGGER: Test received data
            logger.info(f"Sending Data to User Service for remove recipes")

            # Send delete request to User service
            response = requests.delete(f"{USER_SERVICE_URL}/api/collections/recipes/", json=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            recipes = response.json().get('recipes', [])
            titles = [recipe.get('title') for recipe in recipes]
            logger.info(f"Response from User Service: {response.status_code} - {titles}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except ParseError:
            logger.error("Invalid JSON data received for remove user recipes")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)


class UserIngredientsView(APIView):
    # GET request
    def get(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.error(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]

            # LOGGER: Test received token
            logger.info(f"Received Token for Get User Ingredients")

            # Send get request to User service
            response = requests.get(f"{USER_SERVICE_URL}/api/collections/ingredients/", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            ingredients = response.json().get('ingredients', [])
            names = [ingredient.get('name') for ingredient in ingredients]
            logger.info(f"Response from User Service: {response.status_code} - {names}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        
    # POST request
    def post(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.error(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]

            # LOGGER: Test received token
            logger.info(f"Received Token for Add User Ingredients")

            # Read JSON
            data = request.data

            # LOGGER: Test received data
            logger.info(f"Sending Data to User Service for add ingredients")

            # Send post request to User service
            response = requests.post(f"{USER_SERVICE_URL}/api/collections/ingredients/", json=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            ingredients = response.json().get('ingredients', [])
            names = [ingredient.get('name') for ingredient in ingredients]
            logger.info(f"Response from User Service: {response.status_code} - {names}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except ParseError:
            logger.error("Invalid JSON data received for add user ingredients")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        
    # DELETE request
    def delete(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.error(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]

            # LOGGER: Test received token
            logger.info(f"Received Token for Remove User Ingredients")

            # Read JSON
            data = request.data

            # LOGGER: Test received data
            logger.info(f"Sending Data to User Service for remove ingredients")

            # Send delete request to User service
            response = requests.delete(f"{USER_SERVICE_URL}/api/collections/ingredients/", json=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            ingredients = response.json().get('ingredients', [])
            names = [ingredient.get('name') for ingredient in ingredients]
            logger.info(f"Response from User Service: {response.status_code} - {names}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except ParseError:
            logger.error("Invalid JSON data received for remove user ingredients")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
        

class UpdateUserRecipesView(APIView):
    def get(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.error(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]

            # LOGGER: Test received token
            logger.info(f"Received Token for Update User Recipes")

            # Send get request to User service
            response = requests.get(f"{USER_SERVICE_URL}/api/collections/recipes/update/", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            recipes = response.json().get('recipes', [])
            titles = [recipe.get('title') for recipe in recipes]
            logger.info(f"Response from User Service: {response.status_code} - {titles}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)


class UpdateUserIngredientsView(APIView):
    def get(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.error(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            auth_parts = auth_header.split(" ")
            if len(auth_parts) != 2 or auth_parts[0].lower() != "bearer":
                logger.error("Invalid Authorization header format")
                return Response({"message": "Invalid Authorization header format"}, status=401)
            token = auth_parts[1]

            # LOGGER: Test received token
            logger.info(f"Received Token for Update User Ingredients")

            # Send get request to User service
            response = requests.get(f"{USER_SERVICE_URL}/api/collections/ingredients/update/", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()

            # LOGGER : Test response data
            ingredients = response.json().get('ingredients', [])
            names = [ingredient.get('name') for ingredient in ingredients]
            logger.info(f"Response from User Service: {response.status_code} - {names}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)