import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
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


def index(request):
    new_arrivals = Listing.objects.new_arrivals()

    # Exclude user's listings from appearing in new arrivals
    if request.user.is_authenticated:
        new_arrivals = Listing.objects.new_arrivals(user=request.user)

    context = {
        'popular': Category.objects.popular(),
        'new_arrivals': new_arrivals,
        'search_form': SearchForm()
    }
    return render(request, 'auctions/index.html', context)


class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingCreateForm
    template_name = 'auctions/create.html'

    def form_valid(self, form):
        # If the form is valid, save the associated model

        # Calculate end date from duration
        duration = datetime.timedelta(days=form.instance.duration) 
        end_date = datetime.datetime.now() + duration

        # Set model fields omitted from listing form
        form.instance.seller = self.request.user
        form.instance.end_date = end_date
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

        # Determine if listing is in user's watchlist
        is_watched = False
        if self.request.user.is_authenticated:
            is_watched = listing.is_watched(self.request.user)
        
        context['is_watched'] = is_watched
        context['bid_form'] = BidForm()
        return context


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
        """If the form is valid, save the associated model."""

        # Calculate end date from duration
        duration = datetime.timedelta(days=form.instance.duration) 
        end_date = datetime.datetime.now() + duration

        # Set model fields omitted from listing form
        form.instance.seller = self.request.user
        form.instance.end_date = end_date
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
        
        if self.kwargs:
            # Get q_cat parameter from view kwargs (URLconf captured group)
            q_cat = self.kwargs.get('q_cat', None)
        else:
            # Get q_cat parameter from GET request (search form)
            q_cat = self.request.GET.get('q_cat', None)

        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        
        context['categories'] = Category.objects.with_counts(user)
        context['search_form'] = SearchForm()
        context['q_string'] = self.request.GET.get('q_string', None)
        context['q_cat'] = q_cat
        context['total'] = Listing.objects.active(user).count()
        return context

    def get_queryset(self):
        if self.kwargs:
            # Get q_cat parameter from view kwargs (URLconf captured group)
            q_cat = self.kwargs.get('q_cat', None)
            q_string = None
        else:
            # Get query parameters from GET request (search form)
            q_string = self.request.GET.get('q_string', None)
            q_cat = self.request.GET.get('q_cat', None)
        
        queryset = super().get_queryset().exclude(is_active=False)

        # Exclude user's listings
        if self.request.user.is_authenticated:
            queryset = queryset.exclude(seller=self.request.user)
 
        # Match q_string to listing titles
        if q_string:
            queryset = queryset.filter(title__icontains=q_string)

        # Match q_cat string to unique category name
        if q_cat:
            queryset = queryset.filter(category__name__contains=q_cat)
        return queryset


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
    if request.method == 'POST':
        bid_form = BidForm(request.POST)

        if bid_form.is_valid():
            return render(request, 'auctions/data.html', {"context": bid_form.changed_data})

            bid = bid_form.save(commit=False)

            bid.listing = Listing.objects.get(pk=listing_id)
            bid.bidder = request.user
            bid.save()

            messages.success(request, f"Bid successful: ${bid.amount} on {bid.listing.title}.")
            return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))
        else:
            messages.error(request, f"Error: {bid_form.errors}")
            return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,))) 
