import datetime

from django import forms

from auctions.models import Bid
from auctions.models import Category
from auctions.models import Listing


class BidForm(forms.ModelForm):
    amount = forms.DecimalField(
        label = '',
        widget = forms.NumberInput(
            attrs = {
                'class': 'border-0 py-2 w-100 price',
                'name': 'bid_form-amount',
                'placeholder': 'Bid',
            }
        )
    )


    class Meta:
        model = Bid
        fields = ['amount'] 

    def __init__(self, listing, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listing = listing

    def clean(self):
        amount = self.cleaned_data['amount']
        if amount < self.listing.top_bid.amount:
            raise forms.ValidationError("Your bid must be greater than the current top bid.")
        elif amount > self.listing.top_bid.amount + 500:
            raise forms.ValidationError("Your bid cannot be more than $500 higher the current top bid.")


class ListingCreateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=64,
        widget = forms.TextInput(
            attrs = {
                'class': 'border w-100 p-2 bg-white',
                'placeholder': 'Title',
            }
        )
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'border-0 py-2 w-100 price'
            }
        )
    )
    description = forms.CharField(
        max_length=500,
        widget = forms.Textarea(
            attrs = {
                'class': 'border p-3 w-100',
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
                'placeholder': 'Category',
            }
        )
    )
    starting_bid = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'class': 'border-0 py-2 w-100 price',
                'placeholder': 'Starting bid',
            }
        )
    )

    class Meta:
        model = Listing     
        fields = ['title', 'description', 'category', 'image', 'end_date', 'starting_bid']

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        now = datetime.date.today()
        min_end = now + datetime.timedelta(days=3)
        max_end = now + datetime.timedelta(days=31)

        if end_date > max_end or end_date < min_end:
            raise forms.ValidationError("End date must be between 3 and 31 days in the future")
        return end_date


class ListingUpdateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=64,
        widget = forms.TextInput(
            attrs = {
                'class': 'border w-100 p-2 bg-white',
                'placeholder': 'Title',
            }
        )
    )
    description = forms.CharField(
        max_length=500,
        widget = forms.Textarea(
            attrs = {
                'class': 'border p-3 w-100',
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
                'placeholder': 'Category',
            }
        )
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'border-0 py-2 w-100 price'
            }
        )
    )
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'enctype': 'multipart/form-data',
            }
        )
    )

    class Meta:
        model = Listing     
        fields = ['title', 'description', 'category', 'image', 'end_date']

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        now = datetime.date.today()
        min_end = now + datetime.timedelta(days=3)
        max_end = now + datetime.timedelta(days=31)

        if end_date > max_end or end_date < min_end:
            raise forms.ValidationError("End date must be between 3 and 31 days in the future")
        return end_date
    

class SearchForm(forms.Form):
    q_string = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={
                'id': 'inputtext4',
                'class': 'form-control my-2 my-lg-1',
                'placeholder': 'What can we help you find?',
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
