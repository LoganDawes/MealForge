from django.db import models
from django.contrib.auth.models import User

class UserPreferences(models.Model):
    # One-to-one relation with a user
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")

    # Language is list of choices
    language = models.CharField(max_length=20, choices=[("en", "English"), ("es", "Spanish"), ("fr", "French")], default="en")

    # Stores a list of dietary preferences
    diets = models.JSONField(default=list)

    # Stores a list of intolerances
    intolerances = models.JSONField(default=list)

    # Integer calorie limit
    calorie_limit = models.IntegerField(default=2000)

    def __str__(self):
        return f"Preferences for {self.user.username}"