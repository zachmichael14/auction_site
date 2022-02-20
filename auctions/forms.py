from django import forms

from .models import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ["listing", "bidder", "timestamp"]

    amount = forms.CharField(
        label="",
        widget = forms.NumberInput(
            attrs = {
                "class": "border-0 py-2 w-100 price",
                "name": "bid_form-amount",
                "placeholder": "Bid ($0.01-$500.00)"
            }
        )
    )       
