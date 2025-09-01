from django.db import models
from districts.models import District


class School(models.Model):
    name = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='schools')

    def __str__(self):
        return self.name
