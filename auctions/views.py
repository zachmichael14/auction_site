import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .forms import ListingForm, SearchForm
from .models import Category, Listing, Watchlist


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
    form_class = ListingForm
    template_name = 'auctions/create.html'

    def form_valid(self, form):
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
        can_watch = False
        if self.request.user.is_authenticated:
            can_watch = listing.can_watch(self.request.user)
        context['can_watch'] = can_watch
        return context

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

        if self.request.user.is_authenticated:
            # Exclude user's listings
            queryset = queryset.exclude(seller=self.request.user)
        if q_string:
            # Match q_string to listing titles
            queryset = queryset.filter(title__icontains=q_string)
        if q_cat:
            # Match q_cat string to unique category name
            queryset = queryset.filter(category__name__contains=q_cat)
        return queryset


@login_required
def add_to_watchlist(request, listing_id):
    watchlist = Watchlist()
    watchlist.user = request.user
    watchlist.listing = Listing.objects.get(pk=listing_id)
    watchlist.save()

    return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))
