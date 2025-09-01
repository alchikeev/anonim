from django.db import models
from schools.models import School


class ProblemType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Report(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='reports')
    problem_type = models.ForeignKey(ProblemType, on_delete=models.CASCADE, related_name='reports')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.school} - {self.problem_type}"
