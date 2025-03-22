import logging
from django.core.management.base import BaseCommand
from core.models import UserCollections

# Initialize logger
logger = logging.getLogger('django')

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            collections = UserCollections.objects.all()
            for collection in collections:
                # Reduce recipes
                reduced_recipes = [
                    {
                        'id': recipe.get('id'),
                        'title': recipe.get('title'),
                        'image': recipe.get('image')
                    }
                    for recipe in collection.recipes
                ]
                collection.recipes = reduced_recipes

                # Reduce ingredients
                reduced_ingredients = [
                    {
                        'id': ingredient.get('id'),
                        'title': ingredient.get('title'),
                        'image': ingredient.get('image')
                    }
                    for ingredient in collection.ingredients
                ]
                collection.ingredients = reduced_ingredients

                collection.save()
                logger.info(f"Reduced collections for user {collection.user.username}")

            self.stdout.write(self.style.SUCCESS('Successfully reduced collections for all users'))

        # Exception handling
        except Exception as e:
            logger.error(f"Error reducing collections: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Error reducing collections: {str(e)}"))