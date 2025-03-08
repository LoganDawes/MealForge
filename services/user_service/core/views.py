from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from django.contrib.auth.models import User
import logging
import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Initialzes Logger
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class UserView(APIView):
    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER : Test Recieved Data
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

