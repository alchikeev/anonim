from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role-based access."""

    class Roles(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Admin"
        DISTRICT_ADMIN = "district_admin", "District Admin"
        TEACHER = "teacher", "Teacher"

    role = models.CharField(
        max_length=32,
        choices=Roles.choices,
        default=Roles.TEACHER,
        help_text="Designates the user's role within the system.",
    )

    @property
    def is_super_admin(self) -> bool:
        return self.role == self.Roles.SUPER_ADMIN

    @property
    def is_district_admin(self) -> bool:
        return self.role == self.Roles.DISTRICT_ADMIN

    @property
    def is_teacher(self) -> bool:
        return self.role == self.Roles.TEACHER
