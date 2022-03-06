from django.core.exceptions import ValidationError

def validate_bid(amount):
    if amount < 0.01:
        raise ValidationError('Your bid must be greater than or equal to $0.01.')
    if amount > 500.00:
        raise ValidationError('Your bid must be less than or equal to $500.00')
    else:
        return amount