from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserSerializer
import logging

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Initialzes Logger
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(APIView):
    def post(self, request):
        # LOGGER : Test Recieved Data
        logger.info(f"Received Data at user_service: {request.data}")

        # Use User Serializer to create User
        serializer = UserSerializer(data=request.data)

        # Validate User Creation
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User successfully created: {serializer.validated_data}")

            # Authenticate user immediately
            authenticated_user = authenticate(username=user.username, password=request.data["password"])
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
