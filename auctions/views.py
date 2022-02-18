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
        'new_arrivals': new_arrivals

    }
    return render(request, 'auctions/index.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }

    return render(request, 'auctions/listing.html', context)
