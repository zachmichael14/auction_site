from django.urls import path
from . import views as auction_views
app_name = 'auctions'

urlpatterns = [
    path('', auction_views.index, name='index'),
    # path('listing/<int:listing_id>/', auction_views.listing, name='listing'),
    # path('listing/<int:listing_id>/bid/', auction_views.bid, name='bid'),
    path('listing/create/', auction_views.ListingCreateView.as_view(), name='create')
]