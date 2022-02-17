from django.urls import path
from . import views as auction_views

app_name = 'auctions'

urlpatterns = [
    path('', auction_views.index, name='index'),
    path('<int:listing_id>/', auction_views.DetailView.as_view(), name='listing')
]