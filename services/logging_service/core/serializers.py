from rest_framework import serializers
from .models import Log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['service_name', 'log_level', 'message', 'timestamp']