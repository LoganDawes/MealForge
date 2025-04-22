import requests
import logging
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django.contrib.auth.models import User

# REST Framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.exceptions import ParseError

# Initialzes Logger
logger = logging.getLogger('django')

# User Service's URL is in settings.py
USER_SERVICE_URL = settings.USER_SERVICE_URL

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # Read JSON
            data = request.data

            # LOGGER : Test received Data
            logger.info(f"Received Register Data at auth_service")

            # Test for required fields
            required_fields = {"username", "email", "password"}
            if not required_fields.issubset(data):
                logger.error(f"Missing required fields for registration")
                return Response({"message": "Missing required fields"}, status=400)

            # Send post request to User Service
            logger.info(f"Sending data to user service for registering")
            response = requests.post(f"{USER_SERVICE_URL}/api/users/", json=data, timeout=10)
            logger.info(f"Response from user service: {response.status_code} - {response.text}")

            # If user creation failed, return the exact error messages
            if response.status_code != 201:
                return Response(response.json(), status=response.status_code)

            # Retrieve user
            user = User.objects.filter(username=data["username"]).first()
            if not user:
                logger.error(f"User {data['username']} not found for authentication")
                return Response({"message": "User created but not found"}, status=status.HTTP_404_NOT_FOUND)

            # Authenticate user immediately
            authenticated_user = authenticate(username=user.username, password=data["password"])
            if authenticated_user is None:
                logger.error(f"Authentication failed for {user.username} after creation")
                return Response({"message": "User created, but authentication failed"}, status=status.HTTP_400_BAD_REQUEST)
                
            # Generate JWT tokens
            refresh = RefreshToken.for_user(authenticated_user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "User authenticated successfully",
                "access_token": access_token,
                "refresh_token": str(refresh)
            }, status=status.HTTP_201_CREATED)

        # Exception Handling
        except ParseError:
            logger.error(f"Invalid JSON data received for registration")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error when calling user service: {str(e)}")
            return Response({"message": str(e)}, status=500)
            

class UnregisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # Read JSON
            data = request.data

            # LOGGER : Test received Data
            logger.info(f"Received Unregister Data at auth_service")

            # Test for required fields
            required_fields = {"username", "password", "refresh_token"}
            if not required_fields.issubset(data):
                logger.error(f"Missing required fields for unregistration")
                return Response({"message": "Missing required fields"}, status=400)
            
            # Retrieve user
            user = User.objects.filter(username=data["username"]).first()
            if not user:
                logger.error(f"User {data['username']} not found for authentication")
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Authenticate user
            authenticated_user = authenticate(username=user.username, password=data["password"])
            if authenticated_user is None:
                logger.error(f"Authentication failed for {user.username}")
                return Response({"message": "Incorrect Password"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Blacklist the refresh token
            try:
                token = RefreshToken(data["refresh_token"])
                token.blacklist()
                logger.info("Refresh token successfully blacklisted")
            except Exception as e:
                logger.error(f"Failed to blacklist token: {str(e)}")
                return Response({"message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

            # Delete related tokens first
            OutstandingToken.objects.filter(user=user).delete()

            # Send delete request to User Service
            logger.info(f"Sending data to user service for deletion")
            response = requests.delete(f"{USER_SERVICE_URL}/api/users/", json=data, timeout=10)
            logger.info(f"Response from user service: {response.status_code} - {response.text}")
            response.raise_for_status()

            if response.status_code == 200:
                logger.info(f"User {data['username']} successfully unregistered")
                return Response({"message": "User unregistered successfully"}, status=200)
            
            # If user deletion failed
            else:
                logger.error(f"Failed to unregister user {data['username']}. Response from user service: {response.status_code} - {response.text}")
                return Response(response.json(), status=response.status_code)

        # Exception Handling
        except ParseError:
            logger.error(f"Invalid JSON data received for unregistration")
            return Response({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error when calling user service: {str(e)}")
            return Response({"message": str(e)}, status=500)
    

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # Read JSON
            data = request.data

            # LOGGER: Test received data
            logger.info(f"Received Login Data at auth_service")

            # Test for required fields
            required_fields = {"username", "password"}
            if not required_fields.issubset(data):
                logger.error(f"Missing required fields for login")
                return Response({"message": "Missing required fields"}, status=400)

            # Authenticate user
            user = authenticate(username=data["username"], password=data["password"])
            if user is None:
                logger.error(f"Authentication failed for user {data['username']}")
                return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

            # Generate JWT tokens
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)

            return Response({
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": str(refresh_token)
            }, status=200)

        # Exception Handling
        except ParseError:
            logger.error("Invalid JSON data received for login")
            return Response({"message": "Invalid JSON data"}, status=400)
    

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Read JSON
            data = request.data

            # LOGGER: Test received data
            logger.info(f"Received Logout Data at auth_service")

            # Test for required fields
            if "refresh_token" not in data and "user" not in data:
                logger.error("Missing refresh token or user in logout request")
                return Response({"message": "Missing refresh token or user"}, status=400)
            
            # Blacklist the refresh token
            try:
                token = RefreshToken(data["refresh_token"])
                token.blacklist()
                logger.info("Refresh token successfully blacklisted")

                return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Failed to blacklist token: {str(e)}")
                return Response({"message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        # Exception Handling
        except ParseError:
            logger.error("Invalid JSON data received for logout")
            return Response({"message": "Invalid JSON data"}, status=400)
        

class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # Read JSON
            data = request.data

            # LOGGER: Test received data
            logger.info(f"Received Refresh Token Data at auth_service")

            # Test for required fields
            if "refresh_token" not in data:
                logger.error("Missing refresh token in request")
                return Response({"message": "Missing refresh token"}, status=400)

            # Verify and refresh the token
            refresh_token = RefreshToken(data["refresh_token"])
            new_access_token = str(refresh_token.access_token)

            return Response({
                "message": "Token refreshed successfully",
                "access_token": new_access_token,
            }, status=status.HTTP_200_OK)

        # Exception Handling
        except ParseError:
            logger.error("Invalid JSON data received for refresh token")
            return Response({"message": "Invalid JSON data"}, status=400)
