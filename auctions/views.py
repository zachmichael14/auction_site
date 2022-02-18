from django.shortcuts import render
from django.views.generic import DetailView

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


class ListingDetailView(DetailView):
    model = Listing
    pk_url_kwarg = 'listing_id'
    