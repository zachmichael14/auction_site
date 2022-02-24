from django.urls import path, re_path
from . import views as auction_views
app_name = 'auctions'

urlpatterns = [
    path('', auction_views.index, name='index'),
    path('listing/<int:listing_id>/', auction_views.ListingDetailView.as_view(), name='listing'),
    path('browse/', auction_views.BrowseListingView.as_view(), name='browse'),
    path('listing/create/', auction_views.ListingCreateView.as_view(), name='create')
]