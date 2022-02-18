from http.client import NETWORK_AUTHENTICATION_REQUIRED
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Listing, Category


# Create your views here.
def index(request):
    
    context = {
        'popular': Category.objects.popular(),
        'new_arrivals': Listing.objects.new_arrivals(user=request.user)

    }
    return render(request, 'auctions/index.html', context)


class ListingDetailView(DetailView):
    model = Listing
    pk_url_kwarg = 'listing_id'
    