from django import forms

from .models import Bid, Listing, Category


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

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


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing     
        fields = ['title', 'description', 'category', 'image', 'duration', 'starting_bid']

    title = forms.CharField(
        max_length=64,
        widget = forms.TextInput(
            attrs = {
                "class": "border w-100 p-2 bg-white",
                "name": "listing_form-title",
                "placeholder": "Title"
            }
        )
    )
    description = forms.CharField(
        max_length=500,
        widget = forms.Textarea(
            attrs = {
                "class": "border p-3 w-100",
                "name": "listing_form-description",
                "placeholder": "Write details about your product",
            }
        )
    )
    category= forms.ModelChoiceField(
        empty_label="Select a category",
        queryset=Category.objects.all().order_by('category'),
        widget = forms.Select(
            attrs = {
                "id": "inputGroupSelect",
                "class": "w-100",
                "name": "listing_form-category",
                "placeholder": "Category"
            }
        )
    )
    duration = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "border-0 py-2 w-100 price",
                "placeholder": "Duration (3-31 days)",
            }
        )
    )
 
