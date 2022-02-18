from multiprocessing import context
from django.shortcuts import get_object_or_404, render

import auctions

from .models import Category, Listing


def index(request):
    new_arrivals = Listing.objects.new_arrivals()

    # Exclude user's listings from appearing in new arrivals
    if request.user.is_authenticated:
        new_arrivals = Listing.objects.new_arrivals(user=request.user)

    context = {
        'popular': Category.objects.popular(),
        'new_arrivals': new_arrivals,
    }
    return render(request, 'auctions/index.html', context)

def listing(request, listing_id):
    user = request.user
    listing = get_object_or_404(Listing, pk=listing_id)
    is_seller = listing.is_seller()
    is_current_winner = False

    if user.is_authenticated:
        is_seller = listing.is_seller(user=user)
        
        if user == listing.top_bid.bidder:
            is_current_winner = True
        

    context = {
        'listing': listing,
        'is_seller': is_seller,
        'is_current_winner': is_current_winner
    }

    return render(request, 'auctions/listing.html', context)
