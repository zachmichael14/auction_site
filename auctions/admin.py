from django.contrib import admin

from auctions.models import Bid
from auctions.models import Category
from auctions.models import Listing
from auctions.models import Watchlist


class BidTabularInline(admin.TabularInline):
    # Allow editing of bids from listing admin page
    model = Bid


class ListingAdmin(admin.ModelAdmin):
    model = Listing
    list_display = ['title', 'creation_timestamp', 'category']
    list_filter = ['creation_timestamp', 'category']
    inlines = [BidTabularInline]


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['id', 'name']


admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid)
admin.site.register(Watchlist)
