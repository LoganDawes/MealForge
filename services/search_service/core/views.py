import requests
import json
import logging
from django.conf import settings

# REST Framework
from rest_framework.response import Response
from rest_framework.views import APIView

# CSRF Exemption
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
