from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views import View
from django.conf import settings

# Auth Service's URL is in settings.py
AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL

class RegisterUserView(View):
    def post(self, request):
        data = request.POST.dict()  # Assuming form data

        try:
            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/register/", json=data)
            response.raise_for_status()

            # Return response from Auth service
            return JsonResponse(response.json(), status=response.status_code)
        
        except requests.exceptions.RequestException as e:
            return JsonResponse({"message": str(e)}, status=500)
