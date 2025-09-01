import uuid
from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)
    submission_key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self) -> str:
        return self.name
