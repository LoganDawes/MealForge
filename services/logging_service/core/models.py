from django.db import models

class Log(models.Model):
    # Name of the service that generated the log
    service_name = models.CharField(max_length=255)

    # Log level (e.g., INFO, WARNING, ERROR)
    log_level = models.CharField(max_length=50)

    # The actual log message
    message = models.TextField()

    # Timestamp of when the log was created
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.service_name} - {self.log_level}"