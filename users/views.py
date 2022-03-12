from re import template
from auctions.models import Listing
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import UpdateView

from users.forms import UserCreateForm
from users.forms import UserUpdateForm
from users.models import AuctionUser


class UserUpdateView(UpdateView):
    model = AuctionUser
    template_name = 'users/edit_profile.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'image']


def register(request):
    if request.method == 'POST':
        register_form = UserCreateForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. Log in to continue.')
            return redirect('users:login')
    else:
        register_form = UserCreateForm()
    return render(request, 'users/register.html', {
        'register_form': register_form
    })


# @login_required
# def profile(request):
#     u_update_form = UserUpdateForm()

#     context = {
#         'active_listings': Listing.objects.exclude(is_active=False).filter(seller=request.user),
#         'u_update_form': u_update_form,
#     }

#     return render(request, 'users/profile.html', context)
        

class ProfileView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = AuctionUser
    template_name = 'users/profile.html'

    def test_func(self):
        # Ensure user can only view their own profile
        pass

