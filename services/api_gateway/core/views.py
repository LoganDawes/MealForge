from django.shortcuts import render
import requests
import json
import logging
from rest_framework.response import Response
from django.views import View
from rest_framework.views import APIView
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Initialzes Logger
logger = logging.getLogger('django')

# Get Service's URLs in settings.py
AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL
USER_SERVICE_URL = settings.USER_SERVICE_URL

@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(APIView):
    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER : Test recieved data
            logger.info(f"Received Data at api_gateway: {data}")

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/api/register/", json=data, headers={"Content-Type": "application/json"})
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

            # LOGGER : Test recieved data
            logger.info(f"Received Data at api_gateway: {data}")

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/api/unregister/", json=data, headers={"Content-Type": "application/json"})
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
            response = requests.post(f"{AUTH_SERVICE_URL}/api/login/", json=data, headers={"Content-Type": "application/json"})
            logger.info(f"Response from Auth Service: {response.status_code}, {response.text}")

            # LOGGER : Test response data
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
            logger.info(f"Received Data at api_gateway for login: {data}")

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/api/logout/", json=data, headers={"Content-Type": "application/json"})
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
class GetPreferencesView(APIView):
    def get(self, request):
        try:
            # Authorization
            auth_header = request.headers.get('Authorization', None)
            if auth_header is None:
                logger.info(f"Authorization header missing")
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            token = auth_header.split(" ")[1]
            
            # LOGGER: Test received data
            logger.info(f"Received Token for Get Preferences: {token}")

            # Send get request to User service
            response = requests.get(f"{USER_SERVICE_URL}/api/preferences/", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
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
                return Response({"message": "Authorization header missing"}, status=401)

            # Access Token
            token = auth_header.split(" ")[1]
            
            # LOGGER: Test received data
            logger.info(f"Received Token for Update Preferences: {token}")

            # Read the JSON data from the request body
            data = json.loads(request.body)

            # LOGGER: Log data being sent to user service
            logger.info(f"Sending Data to User Service: {data}")

            # Send put request to User service
            response = requests.put(f"{USER_SERVICE_URL}/api/preferences/", json=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
            response.raise_for_status()

            # LOGGER : Test response data
            logger.info(f"Response from User Service: {response.status_code}, {response.text}")

            # Return response from User Service
            return Response(response.json(), status=response.status_code)
        
        # Exception Handling
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return Response({"message": str(e)}, status=500)
