import requests
import json
import logging
from django.conf import settings

# REST Framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

# CSRF Exemption
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Initialzes Logger
logger = logging.getLogger('django')

# User Service's URL is in settings.py
USER_SERVICE_URL = settings.USER_SERVICE_URL

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER : Test Recieved Data
            logger.info(f"Received Register Data at auth_service: {data}")

            # Test for required fields
            required_fields = {"username", "email", "password"}
            if not required_fields.issubset(data):
                logger.error(f"Missing required fields. Received: {data}")
                return Response({"message": "Missing required fields"}, status=400)

            # Send post request to User Service
            logger.info(f"Sending data to user service for registering: {data}")
            response = requests.post(f"{USER_SERVICE_URL}/api/users/", json=data)
            logger.info(f"Response from user service: {response.status_code} - {response.text}")
            response.raise_for_status()

        # Exception Handling
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON data received: {request.body}")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error when calling user service: {str(e)}")
            return Response({"message": str(e)}, status=500)
        
        # If user successfully created, store JWT token
        if response.status_code == 201:
            # Get JWT tokens from create user response
            tokens = response.json()
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")

            # Test for recieved tokens
            if not access_token:
                logger.error("No access token received from user service")
                return Response({"message": "Authentication failed, no token received."}, status=400)

            logger.info(f"User {data['username']} registered successfully. Token stored.")

            return Response({
                "message": "User registered successfully",
                "access_token": access_token,
                "refresh_token": refresh_token
            }, status=201)

        # If user creation failed
        logger.error(f"User creation failed. Response from user service: {response.status_code} - {response.json()}")
        return Response(response.json(), status=response.status_code)
        
@method_decorator(csrf_exempt, name='dispatch')
class UnregisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER : Test Recieved Data
            logger.info(f"Received Unregister Data at auth_service: {data}")

            # Test for required fields
            required_fields = {"username", "password", "refresh_token"}
            if not required_fields.issubset(data):
                logger.error(f"Missing required fields. Received: {data}")
                return Response({"message": "Missing required fields"}, status=400)

            # Send delete request to User Service
            logger.info(f"Sending data to user service for deletion: {data}")
            response = requests.delete(f"{USER_SERVICE_URL}/api/users/", json=data)
            logger.info(f"Response from user service: {response.status_code} - {response.text}")
            response.raise_for_status()

            # If user successfully unregistered, give response
            if response.status_code == 200:
                logger.info(f"User {data['username']} successfully unregistered")
                return Response({"message": "User unregistered successfully"}, status=200)
            
            # If user deletion failed
            else:
                logger.error(f"Failed to unregister user {data['username']}. Response from user service: {response.json()}")
                return Response(response.json(), status=response.status_code)

        # Exception Handling
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON data received: {request.body}")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error when calling user service: {str(e)}")
            return Response({"message": str(e)}, status=500)
    
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER: Test received data
            logger.info(f"Received Login Data at auth_service: {data}")

            # Test for required fields
            required_fields = {"username", "password"}
            if not required_fields.issubset(data):
                logger.error(f"Missing required fields. Received: {data}")
                return Response({"message": "Missing required fields"}, status=400)

            # Forward authentication request to User Service
            response = requests.post(f"{USER_SERVICE_URL}/api/authenticate/", json=data, headers={"Content-Type": "application/json"})
            logger.info(f"Response from user service: {response.status_code}, {response.text}")

            # Handle authentication failure
            if response.status_code != 200:
                return Response(response.json(), status=response.status_code)

            # Extract JWT tokens from user service response
            tokens = response.json()
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")

            if not access_token:
                logger.error("No access token received from user service")
                return Response({"message": "Authentication failed, no token received."}, status=400)

            logger.info(f"User {data['username']} authenticated successfully. Token stored.")

            return Response({
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token
            }, status=200)

        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for login")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error when calling user service: {str(e)}")
            return Response({"message": str(e)}, status=500)
    
@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER: Test received data
            logger.info(f"Received Logout Data at auth_service: {data}")

            # Test for required fields
            if "refresh_token" not in data:
                logger.error("Missing refresh token in logout request")
                return Response({"message": "Missing refresh token"}, status=400)

            # Forward logout request to User Service
            response = requests.post(f"{USER_SERVICE_URL}/api/logout/", json=data, headers={"Content-Type": "application/json"})
            logger.info(f"Response from user service: {response.status_code}, {response.text}")

            return Response(response.json(), status=response.status_code)

        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for login")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error when calling user service: {str(e)}")
            return Response({"message": str(e)}, status=500)
