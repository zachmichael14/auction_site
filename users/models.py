from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

from users.managers import UserManager

class AuctionUser(AbstractUser):
    image = models.ImageField(default='default_profile_pic.jpeg', upload_to='profile_pics')
    objects = UserManager

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Create profile picture thumbnail of size, then save
        size = (300, 300)
        with Image.open(self.image.path) as img:
            if img.height > 300 or img.width > 300:
                img.thumbnail(size)
                img.save(self.image.path)
