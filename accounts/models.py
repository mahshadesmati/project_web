from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars%Y%m%d', default='default-avatar.png')

    def __str__(self):
        return self.username
