from faulthandler import disable
from django import forms
from decimal import Decimal

from .models import Bid, Listing, Category


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

    amount = forms.CharField(
        label = '',
        widget = forms.NumberInput(
            attrs = {
                'class': 'border-0 py-2 w-100 price',
                'name': 'bid_form-amount',
                'placeholder': 'Bid'
            }
        )
    ) 

    def clean(self):
        cleaned_data = super().clean()
        print(self.cleaned_data)
        listing = cleaned_data.get('listing')
        amount = Decimal(cleaned_data.get('amount'))
        if amount < listing.top_bid.amount:
            raise forms.ValidationError({'amount': 'Your bid must be greater than the current top bid.'})
        elif amount > listing.top_bid.amount + 500:
            raise forms.ValidationError({'amount': 'Your bid cannot be more than $500 higher the current top bid.'})


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing     
        fields = ['title', 'description', 'category', 'image', 'duration', 'starting_bid']

    title = forms.CharField(
        max_length=64,
        widget = forms.TextInput(
            attrs = {
                'class': 'border w-100 p-2 bg-white',
                'name': 'listing_form-title',
                'placeholder': 'Title'
            }
        )
    )
    description = forms.CharField(
        max_length=500,
        widget = forms.Textarea(
            attrs = {
                'class': 'border p-3 w-100',
                'name': 'listing_form-description',
                'placeholder': 'Write details about your product',
            }
        )
    )
    category= forms.ModelChoiceField(
        empty_label='Select a category',
        queryset=Category.objects.all().order_by('name'),
        widget = forms.Select(
            attrs = {
                'id': 'inputGroupSelect',
                'class': 'w-100',
                'name': 'listing_form-category',
                'placeholder': 'Category'
            }
        )
    )
    duration = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'border-0 py-2 w-100 price',
                'placeholder': 'Duration (3-31 days)',
            }
        )
    )
    starting_bid = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'border-0 py-2 w-100 price',
                'placeholder': 'Starting bid'
            }
        )
    )
 
class SearchForm(forms.Form):
    q_string = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={
                'id': 'inputtext4',
                'class': 'form-control my-2 my-lg-1',
                'placeholder': 'What can we help you find?'
            }
        )
    )

    q_cat = forms.ModelChoiceField(
        label='',
        required=False,
        empty_label='Select a category',
        to_field_name='name',
        queryset=Category.objects.all().order_by('name'),
        widget = forms.Select(
            attrs = {
                'class': 'w-100 form-control mt-lg-1 mt-md-2',
            }
        )
    )
