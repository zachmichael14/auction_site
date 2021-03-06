from django.urls import path

from . import views as auction_views

app_name = 'auctions'

urlpatterns = [
    path('', auction_views.index, name='index'),
    path('listing/<int:listing_id>/', auction_views.ListingDetailView.as_view(), name='listing'),
    #TODO: Separate out paths using include()
    path('browse/', auction_views.BrowseListingView.as_view(), name='browse'),
    path('browse/?q_cat=<q_cat>/', auction_views.BrowseListingView.as_view(), name='browse'),
    path('listing/create/', auction_views.ListingCreateView.as_view(), name='create'),
    path('listing/<int:listing_id>/wlist_add/', auction_views.add_to_watchlist, name='add_to_watchlist'),
    path('listing/<int:listing_id>/wlist_remove/', auction_views.remove_from_watchlist, name='remove_from_watchlist'),
    path('listing/<int:listing_id>/bid/', auction_views.create_bid, name='create_bid'),
    path('listing/<int:listing_id>/update/', auction_views.ListingUpdateView.as_view(), name='update'),
    path('listing/<int:listing_id>/close/', auction_views.close_listing, name='close'),
    path('listing/<int:listing_id>/delete/', auction_views.ListingDeleteView.as_view(), name='delete'),


]
