from django.db import models


class Report(models.Model):
    class Type(models.TextChoices):
        BULLYING = "bullying", "Bullying"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        NEW = "new", "New"
        REVIEWED = "reviewed", "Reviewed"
        RESOLVED = "resolved", "Resolved"

    school = models.ForeignKey(
        "schools.School", on_delete=models.CASCADE, related_name="reports"
    )
    type = models.CharField(max_length=20, choices=Type.choices)
    message_text = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.school} - {self.get_type_display()}"
