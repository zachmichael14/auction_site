from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import prefetch_related_objects
from PIL import Image



class AuctionUser(AbstractUser):
    image = models.ImageField(default='default_profile_pic.jpeg', upload_to='profile_pics')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Create profile picture thumbnail of size, then save
        size = (300, 300)
        with Image.open(self.image.path) as img:
            if img.height > 300 or img.width > 300:
                img.thumbnail(size)
                img.save(self.image.path)


    def active(self):
        return self.user_listings.filter(is_active=True)

    def closed(self):
        return self.user_listings.filter(is_active=False)

    def won_listings(self):
        return self.won.all()

    def bids(self):
        # Return list rather than QuerySet
        queryset = [obj.listing for obj in self.placed_bids.prefetch_related('listing')]
        # queryset = [obj.listing for obj in self.placed_bids.prefetch_related('listing')]
        return queryset

    def watched(self):
        queryset = [obj.listing for obj in self.user_watchlist.prefetch_related('listing')]
        return queryset
