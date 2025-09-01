from django.db import models
from schools.models import School


class ProblemType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Report(models.Model):
    school = models.ForeignKey(School, related_name="reports", on_delete=models.CASCADE)
    problem_type = models.ForeignKey(ProblemType, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.school} - {self.problem_type}"
