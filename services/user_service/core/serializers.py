from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPreferences

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ["language", "diets", "intolerances", "calorie_limit"]

    # Method to validate the calorie limit
    def validate_calorie_limit(self, value):
        if value < 0 or value > 9999:
            raise serializers.ValidationError("Calorie limit must be between 0 and 9999.")
        return value
