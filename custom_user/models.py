from django.db import models
from django.contrib.auth.models import (AbstractUser)


class CustomUser(AbstractUser):
    bio = models.TextField()

    def __str__(self):
        return self.username

    @property
    def displayName(self):
        return self.first_name + ' ' + self.last_name
