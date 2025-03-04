from django.db import models

# USER
class User(models.Model):
    # Username: unique and under 150 characters
    username = models.CharField(max_length=150, unique=True)
    # Email: unique email
    email = models.EmailField(unique=True)
    # Hashed Password
    password = models.CharField(max_length=255)
    # Active User: Boolean
    is_active = models.BooleanField(default=True)
    # Staff User: Boolean
    is_staff = models.BooleanField(default=False)
    # Date Added: automatically set on user created
    date_added = models.DateTimeField(auto_now_add=True)

    # To string method
    def __str__(self):
        return self.username