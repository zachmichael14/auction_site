from django import forms

<<<<<<< HEAD
from .models import Bid, Listing
=======
from .models import Bid

>>>>>>> 8d8c44d4feaa9b306c3caae9b16b0999ffa3d2e8

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ["listing", "bidder", "timestamp"]

<<<<<<< HEAD
    amount = forms.CharField(
        label="",
=======
    amount = forms.CharField(label="",
>>>>>>> 8d8c44d4feaa9b306c3caae9b16b0999ffa3d2e8
        widget = forms.NumberInput(
            attrs = {
                "class": "border-0 py-2 w-100 price",
                "name": "bid_form-amount",
                "placeholder": "Bid ($0.01-$500.00)"
            }
        )
<<<<<<< HEAD
    )       
=======
    )
>>>>>>> 8d8c44d4feaa9b306c3caae9b16b0999ffa3d2e8
