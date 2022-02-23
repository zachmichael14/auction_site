from re import template
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from django.http import HttpResponseRedirect
import datetime

from .models import Category, Listing

from .forms import ListingForm, SearchForm

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


class BrowseListingView(ListView):
    model = Listing
    template_name = 'auctions/browse.html'
    context_object_name = 'listings'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        q_string = self.request.GET.get('q_string', None)
        q_cat = self.request.GET.get('q_cat', None)

        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        
        context['categories'] = Category.objects.with_counts(user)
        context['search_form'] = SearchForm()
        context['q_string'] = q_string
        context['q_cat'] = q_cat
        return context

    def get_queryset(self):
        q_string = self.request.GET.get('q_string', None)
        q_cat = self.request.GET.get('q_cat', None)

        queryset = super().get_queryset().exclude(is_active=False)
        if q_string:
            queryset = queryset.filter(title__icontains=q_string)
        if q_cat:
            queryset = queryset.filter(category__name__contains=q_cat)
        return queryset