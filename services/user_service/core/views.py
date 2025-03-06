import logging
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

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
            serializer.save()
            logger.info(f"User successfully created: {serializer.validated_data}")
            return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
        
        logger.error(f"User creation failed. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
