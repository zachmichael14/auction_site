from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class AuctionUser(AbstractUser):
    image = models.ImageField(default='default_profile_pic.jpeg', upload_to='profile_pics')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Create profile picture thumbnail of size, then save
        size = (300, 300)
        with Image.open(self.image.path) as img:
            if img.height > 300 or img.width > 300:
                img.thumbnail(size)
                img.save(self.image.path)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('users:profile', kwargs={'pk': self.pk})

    def active(self):
        """Return user's active listings."""
        return self.user_listings.filter(is_active=True)

    def closed(self):
        """Return user's inactive listings."""
        return self.user_listings.filter(is_active=False)

    def won_listings(self):
        """Return listings in which user was top bidder when listing closed."""
        return self.won.all()

    def bids(self):
        """Return list of listings on which user has placed a bid."""
        queryset = [obj.listing for obj in self.placed_bids.prefetch_related('listing')]
        return queryset

    def watched(self):
        """Return list of listings in user's watchlist."""
        queryset = [obj.listing for obj in self.user_watchlist.prefetch_related('listing')]
        return queryset
