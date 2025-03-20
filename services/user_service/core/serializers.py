from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPreferences, UserCollections

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

    class Meta:
        model = UserPreferences
        fields = ["language", "diets", "intolerances", "calorie_limit"]

    def validate_diets(self, value):
        return list(value)

    def validate_intolerances(self, value):
        return list(value)

    # Method to validate the calorie limit
    def validate_calorie_limit(self, value):
        if value < 0 or value > 9999:
            raise serializers.ValidationError("Calorie limit must be between 0 and 9999.")
        return value
    
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
