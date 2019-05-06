# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class IcarusUser(AbstractUser):
    # add additional fields in here
    username = models.TextField(unique=True)
    email = models.TextField(unique=True)
    role = models.TextField() #operator, government_official
    picture_url = models.TextField()

    def __str__(self):
        return self.email

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "picture_url": self.picture_url
        }

    class Meta:
        db_table = 'auth_user'
