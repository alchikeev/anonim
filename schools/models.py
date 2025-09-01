from django.db import models


class District(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class DistrictAdmin(models.Model):
    district = models.ForeignKey(District, related_name="admins", on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=32)

    def __str__(self) -> str:
        return f"{self.district}: {self.chat_id}"


class School(models.Model):
    name = models.CharField(max_length=255)
    district = models.ForeignKey(District, related_name="schools", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Teacher(models.Model):
    school = models.ForeignKey(School, related_name="teachers", on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=32)

    def __str__(self) -> str:
        return f"{self.school}: {self.chat_id}"
