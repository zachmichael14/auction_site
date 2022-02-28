from auctions.models import Listing
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, UserRegistrationForm, UserUpdateForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. Log in to continue.')
            return redirect('users:login')
    else:
        register_form = UserRegistrationForm()
    return render(request, 'users/register.html', {
        'register_form': register_form
    })




@login_required
def profile(request):

    u_update_form = UserUpdateForm()
    p_update_form = ProfileUpdateForm()  

    context = {
        'active_listings': Listing.objects.exclude(is_active=False).filter(seller=request.user),
        'u_update_form': u_update_form,
        'p_update_form': p_update_form
    }

    return render(request, 'users/profile.html', context)
        