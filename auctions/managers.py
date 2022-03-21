from django.db.models import Count
from django.db.models import Manager
from django.db.models import Q


class CategoryManager(Manager):
    def popular(self, n=5):
        # Return n categories containing the highest number of active listings. If tie, return category with lowest pk.
        active_count = Count('listings', filter=Q(listings__is_active=True))
        return self.get_queryset().annotate(actives=active_count).order_by('-actives')[:n]

    def with_counts(self):
        # Return QuerySet of categories and a count of active listings in that category
        count = Count('listings', filter=Q(listings__is_active=True))
        return self.get_queryset().annotate(count=count)

    def with_counts_user(self, user):
        # Exclude user's listings from count and QuerySet 
        count = Count('listings', filter=Q(listings__is_active=True) & ~Q(listings__seller=user))
        return self.get_queryset().annotate(count=count)


class ListingManager(Manager):
    def active(self):
        # Return all active listings
        return self.exclude(is_active=False)

    def active_exclude_user(self, user):
        # Return all active listings excluding user's
        return self.active().exclude(seller=user)

    def recent(self, n=6):
        # Return n most recently created listings
        return self.active().order_by('-creation_timestamp')[:n]
    
    def recent_exclude_user(self, user, n=6):
        # Return n most recently created listings, excluding user's
        return self.active_exclude_user(user).order_by('-creation_timestamp')[:n]





