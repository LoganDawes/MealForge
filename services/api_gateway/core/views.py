from django.shortcuts import render
import requests
import json
import logging
from django.http import JsonResponse
from django.views import View
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Initialzes Logger
logger = logging.getLogger(__name__)

# Auth Service's URL is in settings.py
AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL

@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(View):
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
            return JsonResponse(response.json(), status=response.status_code)
        
        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return JsonResponse({"message": str(e)}, status=500)
        
@method_decorator(csrf_exempt, name='dispatch')
class UnregisterUserView(View):
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
            return JsonResponse(response.json(), status=response.status_code)
        
        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return JsonResponse({"message": str(e)}, status=500)
    
@method_decorator(csrf_exempt, name='dispatch')
class LoginUserView(View):
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
            return JsonResponse(response.json(), status=response.status_code)

        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for login")
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return JsonResponse({"message": str(e)}, status=500)
    
@method_decorator(csrf_exempt, name='dispatch')
class LogoutUserView(View):
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
            return JsonResponse(response.json(), status=response.status_code)

        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for logout")
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {str(e)}")
            return JsonResponse({"message": str(e)}, status=500)
