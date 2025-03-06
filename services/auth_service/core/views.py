from django.shortcuts import render
import requests
import json
import logging
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

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
            required_fields = {"username", "password", "email"}
            if not required_fields.issubset(data):
                return JsonResponse({"message": "Missing required fields"}, status=400)
            
            # Hash password
            data["password"] = make_password(data["password"])

            # Send post request to User Service
            response = requests.post(f"{USER_SERVICE_URL}/api/users/", json=data)
            response.raise_for_status()

        # Exception Handling
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"message": str(e)}, status=500)
        
        # If user successfully created, register with JWT token
        if response.status_code == 201:
                # Use the same credentials to authenticate the user
                username = data["username"]
                password = data["password"]

                # Authenticate the user
                user = authenticate(username=username, password=password)

                if user is None:
                    return JsonResponse({"message": "Authentication failed, invalid credentials."}, status=400)

                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Return success response with JWT token
                return JsonResponse({
                    "message": "User registered successfully",
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                }, status=201)

        return JsonResponse(response.json(), status=response.status_code)
        
        