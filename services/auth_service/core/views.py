from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# User Service's URL is in settings.py
USER_SERVICE_URL = settings.USER_SERVICE_URL

class RegisterView(View):
    def post(self, request):
        data = request.POST.dict()  # Convert incoming data
        data["password"] = make_password(data["password"])  # Hash password

        try:
            # Send post request to User Service
            response = requests.post(f"{USER_SERVICE_URL}/users/", json=data)
            response.raise_for_status()

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
        
        