from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Subject(models.Model):
    course_name = models.CharField(max_length=100, unique=True, null=False)
    course_id = models.CharField(max_length=100, primary_key=True)
    department = models.CharField(max_length=100)
    year_of_study = models.IntegerField()

    def __str__(self):
        id = self.course_id
        return id
