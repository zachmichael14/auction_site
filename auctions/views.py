import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from auctions.forms import BidForm
from auctions.forms import ListingCreateForm
from auctions.forms import ListingUpdateForm
from auctions.forms import SearchForm

from auctions.models import Category 
from auctions.models import Listing 
from auctions.models import Watchlist


class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingCreateForm
    template_name = 'auctions/create.html'

    def form_valid(self, form):
        # Set model fields omitted from listing form
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ListingDetailView(DetailView):
    model = Listing
    template_name = 'auctions/listing.html'
    context_object_name = 'listing'
    pk_url_kwarg = 'listing_id'	

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        listing = self.get_object()
        user = self.request.user
        is_watched = False

        # Determine if listing is in user's watchlist
        if user.is_authenticated:
            is_watched = listing.is_watched(user)
        
        context['is_watched'] = is_watched
        context['bid_form'] = BidForm(listing)
        return context


class ListingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Listing
    pk_url_kwarg = 'listing_id'
    success_url = '/'

    def get_success_url(self):
        user = self.request.user
        return user.get_absolute_url()

    def test_func(self):
        # Ensure only seller can delete listing
        listing = self.get_object()
        return listing.seller == self.request.user
    

class ListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Listing
    template_name = 'auctions/create.html'
    pk_url_kwarg = 'listing_id'

    def get_form_class(self):
        listing = self.get_object()
        self.form_class = ListingUpdateForm

        # Allow editing of starting_bid if bidding hasn't begun
        if listing.top_bid == listing.starting_bid:
            self.form_class = ListingCreateForm
        return self.form_class

    def form_valid(self, form):
        # Set model fields omitted from listing form
        form.instance.seller = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Ensure only seller can edit listing
        listing = self.get_object()
        return listing.seller == self.request.user
    

class BrowseListingView(ListView):
    model = Listing
    template_name = 'auctions/browse.html'
    context_object_name = 'listings'
    paginate_by = 5
    ordering = 'end_date'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        user = self.request.user
        total = Listing.objects.active().count()
        categories = Category.objects.with_counts()
             
        # Exclude user's listings from total and categories
        if user.is_authenticated:
            total = Listing.objects.active_exclude_user(user).count()
            categories = Category.objects.with_counts_user(user)
        
        # Get query parameter from either view kwargs (URLconf captured group) 
        # or GET request (search form)
        if self.kwargs:
            q_cat = self.kwargs.get('q_cat', None)
        else:
            q_cat = self.request.GET.get('q_cat', None)   
        
        context['categories'] = categories
        context['search_form'] = SearchForm()
        context['q_string'] = self.request.GET.get('q_string', None)
        context['q_cat'] = q_cat
        context['total'] = total
        return context

    def get_queryset(self):
        queryset = self.model._default_manager.active()
        user = self.request.user

        # Exclude user's listings
        if user.is_authenticated:
            queryset = self.model._default_manager.active_exclude_user(user)

        # Get query parameters from view kwargs (URLconf captured group; only q_cat captured)
        # or GET request (search form; one or both params)
        if self.kwargs:
            q_cat = self.kwargs.get('q_cat', None)
            q_string = None
        else:
            q_string = self.request.GET.get('q_string', None)
            q_cat = self.request.GET.get('q_cat', None)
 
        # Match query param(s) to listing titles
        if q_string:
            queryset = queryset.filter(title__icontains=q_string)
        if q_cat:
            queryset = queryset.filter(category__name__contains=q_cat)
        return queryset


def index(request):
    # return render(request, 'auctions/data.html')
    user = request.user
    new_arrivals = Listing.objects.recent()

    # Exclude user's listings from appearing in new arrivals
    if user.is_authenticated:
        new_arrivals = Listing.objects.recent_exclude_user(user)

    context = {
        'popular': Category.objects.popular(),
        'new_arrivals': new_arrivals,
        'search_form': SearchForm()
    }
    return render(request, 'auctions/index.html', context)

@login_required
def add_to_watchlist(request, listing_id):
    if request.method == 'POST':
        watchlist = Watchlist()
        watchlist.user = request.user
        watchlist.listing = Listing.objects.get(pk=listing_id)
        watchlist.save()

        messages.success(request, f"{watchlist.listing.title} added to your watchlist.")
        return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))

@login_required
def remove_from_watchlist(request, listing_id):
    if request.method == 'POST':
        watchlist = Watchlist.objects.get(user=request.user, listing=listing_id)
        watchlist.delete()

        messages.warning(request, f"{watchlist.listing.title} removed from your watchlist.")
        return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))

@login_required
def create_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == 'POST':
        bid_form = BidForm(listing=listing, data=request.POST)
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)

            # Set fields that were excluded from form
            bid.listing = listing
            bid.bidder = request.user
            bid.save()

            messages.success(request, f"Bid successful: ${bid.amount} on {bid.listing.title}.")
            return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))

    context = {
        'listing': listing,
        'bid_form': bid_form
    }
    return render(request, 'auctions/listing.html', context)

@login_required
def close_listing(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        if listing.seller == request.user:
            listing.winner = listing.get_winner()
            listing.is_active = False
            listing.save()
            return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))
        else:
            raise PermissionDenied