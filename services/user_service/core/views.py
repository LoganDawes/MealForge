import requests
import json
import logging
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# REST Framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

# Models & Serializers
from django.contrib.auth.models import User
from .models import UserPreferences
from .serializers import UserSerializer, UserPreferencesSerializer

# CSRF Exemption
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Initialzes Logger
logger = logging.getLogger('django')

@method_decorator(csrf_exempt, name='dispatch')
class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    # POST Request
    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER : Test received Data
            logger.info(f"Received Data for user creation: {data}")

            # Use User Serializer to create User
            serializer = UserSerializer(data=data)

            # Validate User Creation
            if serializer.is_valid():
                user = serializer.save()
                logger.info(f"User successfully created: {serializer.validated_data}")

                # Authenticate user immediately
                authenticated_user = authenticate(username=user.username, password=data["password"])
                if authenticated_user is None:
                    logger.error(f"Authentication failed for {user.username} after creation")
                    return Response({"message": "User created, but authentication failed"}, status=status.HTTP_400_BAD_REQUEST)
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(authenticated_user)
                access_token = str(refresh.access_token)

                return Response({
                    "message": "User created successfully",
                    "access_token": access_token,
                    "refresh_token": str(refresh)
                }, status=status.HTTP_201_CREATED)
            
            logger.error(f"User creation failed. Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for creation")
            return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during user creation: {str(e)}")
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # DELETE Request
    def delete(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER: Test received data
            logger.info(f"Received Data for user deletion: {data}")

            # Retrieve user
            user = User.objects.filter(username=data["username"]).first()
            if not user:
                logger.error(f"User {data['username']} not found for deletion")
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Authenticate user
            authenticated_user = authenticate(username=user.username, password=data["password"])
            if authenticated_user is None:
                logger.error(f"Authentication failed for {user.username} after creation")
                return Response({"message": "User found, but authentication failed"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Blacklist the refresh token
            try:
                token = RefreshToken(data["refresh_token"])
                token.blacklist()
                logger.info("Refresh token successfully blacklisted")
            except Exception as e:
                logger.error(f"Failed to blacklist token: {str(e)}")
                return Response({"message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

            # Delete user
            user.delete()
            logger.info(f"User {data['username']} successfully deleted")
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)

        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for deletion")
            return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during user deletion: {str(e)}")
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@method_decorator(csrf_exempt, name='dispatch')
class AuthenticateUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # Read JSON
            data = request.data

            # LOGGER: Test received data
            logger.info(f"Received authentication request at user_service: {data}")

            # Authenticate user
            user = authenticate(username=data["username"], password=data["password"])
            if user is None:
                logger.error(f"Authentication failed for user {data['username']}")
                return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            logger.info(f"User {data['username']} authenticated successfully. Tokens generated.")

            return Response({
                "message": "Authentication successful",
                "access_token": access_token,
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)

        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for authentication")
            return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during user authentication: {str(e)}")
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@method_decorator(csrf_exempt, name='dispatch')
class LogoutUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # Read JSON
            data = request.data

            # LOGGER: Test received data
            logger.info(f"Received logout request at user_service: {data}")

            # Ensure refresh token is provided
            if "refresh_token" not in data:
                logger.error("Missing refresh token in logout request")
                return Response({"message": "Missing refresh token"}, status=status.HTTP_400_BAD_REQUEST)

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
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for logout")
            return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during logout: {str(e)}")
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@method_decorator(csrf_exempt, name='dispatch')
class UserPreferencesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # GET Request
    def get(self, request):
        try:
            # Fetch or create default preferences for the authenticated user
            preferences, created = UserPreferences.objects.get_or_create(user=request.user)
            serializer = UserPreferencesSerializer(preferences)

            # LOGGER: Test received data
            logger.info(f"Retrieved preferences for user {request.user.username} (Created: {created})")

            return Response(serializer.data, status=status.HTTP_200_OK)

        # Exception Handling
        except Exception as e:
            logger.error(f"Unexpected error retrieving preferences for user {request.user.username}: {str(e)}")
            return Response({"message": "An error occurred while retrieving preferences."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PUT Request
    def put(self, request):
        try:
            # Fetch or create default preferences for the authenticated user
            preferences, _ = UserPreferences.objects.get_or_create(user=request.user)

            # LOGGER: Test received data
            logger.info(f"Received update request for user {request.user.username}: {request.data}")

            # Validate and update preferences
            serializer = UserPreferencesSerializer(preferences, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated preferences for user {request.user.username}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # Log validation errors
            logger.error(f"Validation failed for user {request.user.username}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Exception Handling
        except Exception as e:
            logger.error(f"Unexpected error updating preferences for user {request.user.username}: {str(e)}")
            return Response({"message": "An error occurred while updating preferences."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


