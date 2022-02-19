from django.core.exceptions import ValidationError

def validate_bid(bid, listing):
    if bid < listing.top_bid:
        raise ValidationError('Your bid must be higher than the current top bid.')
    elif bid < 0.01:
        raise ValidationError('Your bid must be greater than or equal to $0.01.')
    elif bid > 500.00:
        raise ValidationError('Your bid must be less than or equal to $500.00')
    else:
        return bid