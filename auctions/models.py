from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT

from .managers import CategoryManager, ListingManager


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.category


class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=CASCADE, related_name='user_listings')
    category = models.ForeignKey(Category, on_delete=PROTECT, related_name='listings')
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)
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


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=CASCADE, related_name='placed_bids')
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[
            MinValueValidator(0.01, message='Bid must be between $0.01 and $500.00 (inclusive).'),
            MaxValueValidator(500.00, message='Bid must be between $0.01 and $500.00 (inclusive).')
        ]
    )

    def __str__(self):
        return str(self.amount)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    listing = models.ForeignKey(Listing, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user} watching post {self.listing}'
