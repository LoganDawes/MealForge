from django.shortcuts import render
import requests
import json
import logging
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Initialzes Logger
logger = logging.getLogger(__name__)

# User Service's URL is in settings.py
USER_SERVICE_URL = settings.USER_SERVICE_URL

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER : Test Recieved Data
            logger.info(f"Received Data at auth_service: {data}")

            # Test for required fields
            required_fields = {"username", "email", "password"}
            if not required_fields.issubset(data):
                logger.error(f"Missing required fields. Received: {data}")
                return JsonResponse({"message": "Missing required fields"}, status=400)

            # Send post request to User Service
            logger.info(f"Sending data to user service: {data}")
            response = requests.post(f"{USER_SERVICE_URL}/api/users/", json=data)
            logger.info(f"Response from user service: {response.status_code} - {response.text}")
            response.raise_for_status()

        # Exception Handling
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON data received: {request.body}")
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error when calling user service: {str(e)}")
            return JsonResponse({"message": str(e)}, status=500)
        
        # If user successfully created, store JWT token
        if response.status_code == 201:
            # Get JWT tokens from create user response
            tokens = response.json()
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")

            # Test for recieved tokens
            if not access_token:
                logger.error("No access token received from user service")
                return JsonResponse({"message": "Authentication failed, no token received."}, status=400)

            logger.info(f"User {data['username']} registered successfully. Token stored.")

            return JsonResponse({
                "message": "User registered successfully",
                "access_token": access_token,
                "refresh_token": refresh_token
            }, status=201)

        logger.error(f"User creation failed. Response from user service: {response.status_code} - {response.json()}")
        return JsonResponse(response.json(), status=response.status_code)
        
class UnregisterView(View):
    def post(self, request):
        # NYI
        return None
    
class LoginView(View):
    def post(self, request):
        # NYI
        return None
    
class LogoutView(View):
    def post(self, request):
        # NYI
        return None
