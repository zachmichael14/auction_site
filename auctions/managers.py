from tracemalloc import is_tracing
from django.db.models import Count, Manager, Q


class CategoryManager(Manager):
    def popular(self, n=5):
        # Return n categories containing the highest number of active listings. If tie, return category with lowest pk.
        active_count = Count('listings', filter=Q(listings__is_active=True))
        return self.get_queryset().annotate(actives=active_count).order_by('-actives')[:n]

    def with_counts(self, user=None):
        # Return QuerySet of categories and a count of active listings in that category
        count = Count('listings', filter=Q(listings__is_active=True))
        # If user, exclude user's listings from both QuerySet and count
        if user:
            count = Count('listings', filter=Q(listings__is_active=True) & ~Q(listings__seller=user))
        return self.get_queryset().annotate(count=count)

class ListingManager(Manager):
    def active(self, user=None):
        # Return active listings. If user, exclude user's listings from results
        if user:
            return self.exclude(is_active=False).exclude(seller=user)
        return self.exclude(is_active=False)

    def new_arrivals(self, user=None, n=6):
        # Return n most recently created listings
        return self.active(user).order_by('-creation_timestamp')[:n]

