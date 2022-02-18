from django.db.models import Count, Manager, Q


class CategoryManager(Manager):
    def popular(self, n=5):
        # Return n categories containing the highest number of active listings. If tie, return category with lowest pk.
        active_count = Count('listings', filter=Q(listings__is_active=True))
        return self.get_queryset().annotate(actives=active_count).order_by('-actives')[:n]


class ListingManager(Manager):
    def new_arrivals(self, user=None, n=6):
        # Return n most recently created listings
        if user:
            return self.exclude(is_active=False).exclude(seller=user).order_by('-creation_timestamp')[:n]
        return self.exclude(is_active=False).order_by('-creation_timestamp')[:n]
