import requests
import json
import logging
from django.conf import settings

# REST Framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

# Models & Serializers
from django.contrib.auth.models import User
from .models import UserPreferences, UserCollections
from .serializers import UserSerializer, UserPreferencesSerializer, UserCollectionsSerializer

# CSRF Exemption
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Initialzes Logger
logger = logging.getLogger('django')

# Get Service's URLs in settings.py
INTEGRATION_SERVICE_URL = settings.INTEGRATION_SERVICE_URL

@method_decorator(csrf_exempt, name='dispatch')
class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    # POST Request
    def post(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER : Test received Data
            logger.info(f"Received Data for user creation: {data}")

            # Use User Serializer to create User
            serializer = UserSerializer(data=data)

            # Validate User Creation
            if serializer.is_valid():
                user = serializer.save()
                logger.info(f"User successfully created: {serializer.validated_data}")

                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
            
            logger.error(f"User creation failed. Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for creation")
            return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during user creation: {str(e)}")
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # DELETE Request
    def delete(self, request):
        try:
            # Read JSON
            data = json.loads(request.body)

            # LOGGER: Test received data
            logger.info(f"Received Data for user deletion: {data}")

            # Retrieve user
            user = User.objects.filter(username=data["username"]).first()
            if not user:
                logger.error(f"User {data['username']} not found for deletion")
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # Delete user
            user.delete()
            logger.info(f"User {data['username']} successfully deleted")
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)

        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for deletion")
            return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during user deletion: {str(e)}")
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@method_decorator(csrf_exempt, name='dispatch')
class UserPreferencesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # GET Request
    def get(self, request):
        try:
            # Fetch or create default preferences for the authenticated user
            preferences, created = UserPreferences.objects.get_or_create(user=request.user)
            serializer = UserPreferencesSerializer(preferences)

            # LOGGER: Test received data
            logger.info(f"Retrieved preferences for user {request.user.username} (Created: {created})")

            return Response(serializer.data, status=status.HTTP_200_OK)

        # Exception Handling
        except Exception as e:
            logger.error(f"Unexpected error retrieving preferences for user {request.user.username}: {str(e)}")
            return Response({"message": "An error occurred while retrieving preferences."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PUT Request
    def put(self, request):
        try:
            # Fetch or create default preferences for the authenticated user
            preferences, _ = UserPreferences.objects.get_or_create(user=request.user)

            # LOGGER: Test received data
            logger.info(f"Received update request for user {request.user.username}: {request.data}")

            # Validate and update preferences
            serializer = UserPreferencesSerializer(preferences, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated preferences for user {request.user.username}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # Log validation errors
            logger.error(f"Validation failed for user {request.user.username}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Exception Handling
        except Exception as e:
            logger.error(f"Unexpected error updating preferences for user {request.user.username}: {str(e)}")
            return Response({"message": "An error occurred while updating preferences."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@method_decorator(csrf_exempt, name='dispatch')
class UserRecipesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # GET Request
    def get(self, request):
        try:
            # Fetch or create default collections for the authenticated user
            collections, created = UserCollections.objects.get_or_create(user=request.user)
            serializer = UserCollectionsSerializer(collections, fields=['recipes'])

            # LOGGER: Test received data
            logger.info(f"Retrieved recipes for user {request.user.username} (Created: {created})")

            return Response(serializer.data, status=status.HTTP_200_OK)

        # Exception Handling
        except Exception as e:
            logger.error(f"Unexpected error retrieving recipes for user {request.user.username}: {str(e)}")
            return Response({"message": "An error occurred while retrieving recipes."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # POST Request
    def post(self, request):
        try:
            # Fetch or create default collections for the authenticated user
            collections, _ = UserCollections.objects.get_or_create(user=request.user)

            # LOGGER: Test received data
            logger.info(f"Received add request for user {request.user.username}: {request.data}")

            # Add new recipe to collections
            new_recipe = request.data.get('recipe')
            if new_recipe:
                collections.recipes.append(new_recipe)
                collections.save()

                # LOGGER: Updated collections
                logger.info(f"Added recipe for user {request.user.username}: {new_recipe}")
                return Response({"recipes": collections.recipes}, status=status.HTTP_200_OK)
            else:
                logger.error(f"No recipe provided in the request for user {request.user.username}")
                return Response({"message": "No recipe provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Exception Handling
        except Exception as e:
            logger.error(f"Unexpected error adding recipe for user {request.user.username}: {str(e)}")
            return Response({"message": "An error occurred while adding recipe."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE Request
    def delete(self, request):
        try:
            # Fetch or create default collections for the authenticated user
            collections, _ = UserCollections.objects.get_or_create(user=request.user)

            # LOGGER: Test received data
            logger.info(f"Received delete request for user {request.user.username}: {request.data}")

            # Remove recipe from collections
            recipe_to_remove = request.data.get('recipe_id')
            if recipe_to_remove:
                if any(recipe.get('id') == recipe_to_remove for recipe in collections.recipes):
                    collections.recipes = [recipe for recipe in collections.recipes if recipe.get('id') != recipe_to_remove]
                    collections.save()

                    # LOGGER: Updated collections
                    logger.info(f"Removed recipe for user {request.user.username}: {recipe_to_remove}")
                    return Response({"recipes": collections.recipes}, status=status.HTTP_200_OK)
                else:
                    logger.error(f"Recipe with id {recipe_to_remove} not found in collections for user {request.user.username}")
                    return Response({"message": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                logger.error(f"No recipe provided in the request for user {request.user.username}")
                return Response({"message": "No recipe provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Exception Handling
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received for deletion")
            return Response({"message": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error removing recipe for user {request.user.username}: {str(e)}")
            return Response({"message": "An error occurred while removing recipe."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class UserIngredientsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # GET Request
    def get(self, request):
        try:
            # Fetch or create default collections for the authenticated user
            collections, created = UserCollections.objects.get_or_create(user=request.user)
            serializer = UserCollectionsSerializer(collections, fields=['ingredients'])

            # LOGGER: Test received data
            logger.info(f"Retrieved ingredients for user {request.user.username} (Created: {created})")

            return Response(serializer.data, status=status.HTTP_200_OK)

        # Exception Handling
        except Exception as e:
            logger.error(f"Unexpected error retrieving ingredients for user {request.user.username}: {str(e)}")
            return Response({"message": "An error occurred while retrieving ingredients."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # POST Request
    def post(self, request):
        try:
            # Fetch or create default collections for the authenticated user
            collections, _ = UserCollections.objects.get_or_create(user=request.user)

            # LOGGER: Test received data
            logger.info(f"Received add request for user {request.user.username}: {request.data}")

            # Add new ingredient to collections
            new_ingredient = request.data.get('ingredient')
            if new_ingredient:
                collections.ingredients.append(new_ingredient)
                collections.save()

                # LOGGER: Updated collections
                logger.info(f"Added ingredient for user {request.user.username}: {new_ingredient}")
                return Response({"ingredients": collections.ingredients}, status=status.HTTP_200_OK)
            else:
                logger.error(f"No ingredient provided in the request for user {request.user.username}")
                return Response({"message": "No ingredient provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Exception Handling
        except Exception as e:
            logger.error(f"Unexpected error adding ingredient for user {request.user.username}: {str(e)}")
            return Response({"message": "An error occurred while adding ingredient."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE Request
    def delete(self, request):
        try:
            # Fetch or create default collections for the authenticated user
            collections, _ = UserCollections.objects.get_or_create(user=request.user)

            # LOGGER: Test received data
            logger.info(f"Received delete request for user {request.user.username}: {request.data}")

            # Remove ingredient from collections
            ingredient_to_remove = request.data.get('ingredient_id')
            if ingredient_to_remove:
                if any(ingredient.get('id') == ingredient_to_remove for ingredient in collections.ingredients):
                    collections.ingredients = [ingredient for ingredient in collections.ingredients if ingredient.get('id') != ingredient_to_remove]
                    collections.save()

                    # LOGGER: Updated collections
                    logger.info(f"Removed ingredient for user {request.user.username}: {ingredient_to_remove}")
                    return Response({"ingredients": collections.ingredients}, status=status.HTTP_200_OK)
                else:
                    logger.error(f"Ingredient with id {ingredient_to_remove} not found in collections for user {request.user.username}")
                    return Response({"message": "Ingredient not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                logger.error(f"No ingredient provided in the request for user {request.user.username}")
                return Response({"message": "No ingredient provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Exception Handling
        except Exception as e:
            logger.error(f"Unexpected error removing ingredient for user {request.user.username}: {str(e)}")
            return Response({"message": "An error occurred while removing ingredient."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@method_decorator(csrf_exempt, name='dispatch')
class UpdateRecipesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Fetch or create default collections for the authenticated user
            collections, _ = UserCollections.objects.get_or_create(user=request.user)
            updated_recipes = []

            for recipe in collections.recipes:
                if set(recipe.keys()) == {'id', 'title', 'image'}:
                    # Make a GET request to the integrations service to get full recipe information
                    logger.info(f"Updating recipe {recipe} for user {request.user.username}")
                    response = requests.get(f"{INTEGRATION_SERVICE_URL}/api/recipes/{recipe['id']}/")
                    response.raise_for_status()

                    #LOGGER: Test received data
                    logger.info(f"Response from Integration service: {response.status_code}, {response.text}")

                    if response.status_code == 200:
                        full_recipe = response.json()
                        updated_recipes.append(full_recipe)
                    else:
                        updated_recipes.append(recipe)
                else:
                    logger.info(f"Recipe {recipe} appending without update")
                    updated_recipes.append(recipe)

            collections.recipes = updated_recipes
            collections.save()

            logger.info(f"Updated recipes for user {request.user.username}")
            return Response({"recipes": collections.recipes}, status=status.HTTP_200_OK)

        # Exception Handling
        except Exception as e:
            logger.error(f"Unexpected error updating recipes for user {request.user.username}: {str(e)}")
            return Response({"message": "An error occurred while updating recipes."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@method_decorator(csrf_exempt, name='dispatch')
class UpdateIngredientsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Fetch or create default collections for the authenticated user
            collections, _ = UserCollections.objects.get_or_create(user=request.user)
            updated_ingredients = []

            for ingredient in collections.ingredients:
                if set(ingredient.keys()) == {'id', 'title', 'image'}:
                    # Make a GET request to the integrations service to get full ingredient information
                    response = requests.get(f"{INTEGRATION_SERVICE_URL}/api/ingredients/{ingredient['id']}/")
                    response.raise_for_status()

                    #LOGGER: Test received data
                    logger.info(f"Response from Integration service: {response.status_code}, {response.text}")
                    
                    if response.status_code == 200:
                        full_ingredient = response.json()
                        updated_ingredients.append(full_ingredient)
                    else:
                        updated_ingredients.append(ingredient)
                else:
                    updated_ingredients.append(ingredient)

            collections.ingredients = updated_ingredients
            collections.save()

            logger.info(f"Updated ingredients for user {request.user.username}")
            return Response({"ingredients": collections.ingredients}, status=status.HTTP_200_OK)

        # Exception Handling
        except Exception as e:
            logger.error(f"Unexpected error updating ingredients for user {request.user.username}: {str(e)}")
            return Response({"message": "An error occurred while updating ingredients."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)