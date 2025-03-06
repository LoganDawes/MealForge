from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
from django.views import View
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Auth Service's URL is in settings.py
AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL

@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(View):
    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # Send post request to Auth service
            response = requests.post(f"{AUTH_SERVICE_URL}/register/", json=data, headers={"Content-Type": "application/json"})
            response.raise_for_status()

            # Return response from Auth service
            return JsonResponse(response.json(), status=response.status_code)
        
        # Exception Handling
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"message": str(e)}, status=500)
