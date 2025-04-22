import requests

from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User
from .models import UserPreferences, UserCollections
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

HUNTER_API_KEY = settings.HUNTER_API_KEY
HUNTER_API_URL = settings.HUNTER_API_URL

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        # Check if the email is already in use
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use. Please use a different email.")

        # Validate email format
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        
        try:
            response = requests.get(
                f"{HUNTER_API_URL}",
                params={"email": value, "api_key": HUNTER_API_KEY},
                timeout=10
            )
            response_data = response.json()

            # Check if the email is valid
            if response.status_code != 200 or response_data.get("data", {}).get("status") != "valid":
                raise serializers.ValidationError("Invalid email address. Please provide a valid email.")
        except requests.exceptions.RequestException as e:
            raise serializers.ValidationError(f"Error validating email: {str(e)}")

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    

class UserPreferencesSerializer(serializers.ModelSerializer):
    DIET_CHOICES = [
        ("Gluten free", "Gluten Free"),
        ("Ketogenic", "Ketogenic"),
        ("Vegetarian", "Vegetarian"),
        ("Lacto-vegetarian", "Lacto-Vegetarian"),
        ("Ovo-vegetarian", "Ovo-Vegetarian"),
        ("Vegan", "Vegan"),
        ("Pescetarian", "Pescetarian"),
        ("Paleo", "Paleo"),
        ("Primal", "Primal"),
        ("Low fodmap", "Low FODMAP"),
        ("Whole30", "Whole30"),
    ]

    INTOLERANCE_CHOICES = [
        ("Dairy", "Dairy"),
        ("Egg", "Egg"),
        ("Gluten", "Gluten"),
        ("Grain", "Grain"),
        ("Peanut", "Peanut"),
        ("Seafood", "Seafood"),
        ("Sesame", "Sesame"),
        ("Shellfish", "Shellfish"),
        ("Soy", "Soy"),
        ("Sulfite", "Sulfite"),
        ("Tree nut", "Tree Nut"),
        ("Wheat", "Wheat"),
    ]

    diets = serializers.MultipleChoiceField(choices=DIET_CHOICES)
    intolerances = serializers.MultipleChoiceField(choices=INTOLERANCE_CHOICES)
    calorie_limit = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = UserPreferences
        fields = ["language", "diets", "intolerances", "calorie_limit"]

    def validate_diets(self, value):
        return list(value)

    def validate_intolerances(self, value):
        return list(value)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        # Handle empty or invalid calorie_limit
        calorie_limit = data.get("calorie_limit")
        if calorie_limit in [None, ""]:
            data["calorie_limit"] = 9999  # Default to 9999 if empty
        else:
            try:
                data["calorie_limit"] = int(calorie_limit)  # Convert to integer
            except ValueError:
                data["calorie_limit"] = 9999  # Default to 9999 if invalid
        return data
    
class UserCollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCollections
        fields = ["recipes", "ingredients"]

    # Custom init method to filter fields
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(UserCollectionsSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
