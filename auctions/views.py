from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView

from django.http import HttpResponseRedirect
import datetime

from .models import Category, Listing

from .forms import ListingForm

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


class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    template_name = 'auctions/create.html'

    def form_valid(self, form):
        duration = datetime.timedelta(days=form.instance.duration) 
        end_date = datetime.datetime.now() + duration

        form.instance.seller = self.request.user
        form.instance.end_date = end_date

        
        return super().form_valid(form)


def listing(request, listing_id):
    user = request.user
    listing = get_object_or_404(Listing, pk=listing_id)
    # is_seller = listing.is_seller()
    # is_current_winner = False

    # if user.is_authenticated:
    #     is_seller = listing.is_seller(user=user)
        
    #     if user == listing.top_bid.bidder:
    #         is_current_winner = True
        

    context = {
        'listing': listing,
        # 'is_seller': is_seller,
        # 'is_current_winner': is_current_winner,
        # 'bid_form': BidForm()
    }

    return render(request, 'auctions/listing.html', context)
