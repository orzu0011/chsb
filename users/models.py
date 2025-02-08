from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Administrator"),
        ("teacher", "O‘qituvchi"),
        ("student", "O‘quvchi"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return self.username