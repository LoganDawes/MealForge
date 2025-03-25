import logging

# REST Framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Models & Serializers
from .serializers import LogSerializer

# CSRF Exemption
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Initialize Logger
logger = logging.getLogger('django')

class LogView(APIView):
    def post(self, request):
        try:
            # Use Log serializer to create Log entry
            serializer = LogSerializer(data=request.data)

            # Validate Log creation
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Log created: {serializer.data.service_name} - {serializer.data.log_level}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            logger.error(f"Log creation failed. Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Exception Handling
        except Exception as e:
            logger.exception(f"Exception occurred: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)