from django.conf import settings
from django.db import models


class Message(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In Progress"
        RESOLVED = "resolved", "Resolved"

    title = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="messages",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    message = models.ForeignKey(
        Message, related_name="comments", on_delete=models.CASCADE
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
