from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT

from .managers import CategoryManager, ListingManager

from .validators import validate_bid


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name


class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=CASCADE, related_name='user_listings')
    category = models.ForeignKey(Category, on_delete=PROTECT, related_name='listings')
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(
        validators=[
            MinValueValidator(3, message='Duration must be between 3 and 31 days (inclusive).'),
            MaxValueValidator(31, message='Duration must be between 3 and 31 days (inclusive).')
        ]
    )
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=PROTECT, related_name='won')
    objects = ListingManager()

    def __str__(self):
        return f'{self.title} (ID: {self.id}) by {self.seller}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('auctions:listing', kwargs={'listing_id': self.pk})

    @property
    def top_bid(self):
        # Check for bids on listing
        if Bid.objects.filter(listing=self.id).exists():
            # If bids, return highest
            return Bid.objects.filter(listing=self.id).order_by('-amount').first()
        return self.starting_bid

    def is_seller(self, user=None):
        if user == self.seller:
            return True
        return False

    


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=CASCADE, related_name='placed_bids')
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        # validators=[validate_bid]
    )

    def __str__(self):
        return str(self.amount)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        top_bid = self.listing.top_bid
        if amount < top_bid:
            raise ValidationError('Your bid must be greater than the current top bid.')


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    listing = models.ForeignKey(Listing, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user} watching post {self.listing}'
