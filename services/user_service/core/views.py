import requests
import json
import logging
from django.conf import settings

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

                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
            
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


