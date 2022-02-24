from django.contrib import admin
from .models import Category, Listing, Bid, Watchlist
# Register your models here.

# Allow editing of bids from listing admin page
class BidTabularInline(admin.TabularInline):
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
