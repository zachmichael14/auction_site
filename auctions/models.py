from users.models import AuctionUser
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from auctions.managers import CategoryManager
from auctions.managers import ListingManager


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name


class Listing(models.Model):
    seller = models.ForeignKey(AuctionUser, on_delete=models.CASCADE, related_name='user_listings')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='listings')
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(blank=True, default='no_image.png', upload_to='listing_pics')
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(
        validators=[
            MinValueValidator(3, message='Duration must be between 3 and 31 days (inclusive).'),
            MaxValueValidator(31, message='Duration must be between 3 and 31 days (inclusive).'),
        ]
    )
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(AuctionUser, blank=True, null=True, on_delete=models.PROTECT, related_name='won')

    objects = ListingManager()

    def __str__(self):
        return f'{self.title} (ID: {self.id}) by {self.seller}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('auctions:listing', kwargs={'listing_id': self.pk})

    def get_winner(self):
        """
        Return current highest bidder. 
        Return None if no bids have been placed.
        """
        if self.top_bid == self.starting_bid:
            return None
        return self.top_bid.bidder

    def is_watched(self, user):
        """Return True if listing is in user's watchlist."""
        if Watchlist.objects.filter(user=user, listing=self).exists():
            return True
        return False

    @property
    def top_bid(self):
        """Return current highest bid."""
        # Check for bids on listing
        if Bid.objects.filter(listing=self.id).exists():
            # If bids, return highest
            return Bid.objects.filter(listing=self.id).order_by('-amount').first()
        return self.starting_bid

    
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(AuctionUser, on_delete=models.CASCADE, related_name='placed_bids')
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(
        max_digits=19, 
        decimal_places=2, 
    )

    def __str__(self):
        return str(self.amount)


class Watchlist(models.Model):
    user = models.ForeignKey(AuctionUser, on_delete=models.CASCADE, related_name='user_watchlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} watching post {self.listing}'