from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from users.forms import UserCreateForm
from users.forms import UserUpdateForm
from users.models import AuctionUser


class UserView(LoginRequiredMixin, ListView):
    model = AuctionUser
    template_name = 'users/profile.html'
    context_object_name = 'listings'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        counts = {
            'active': user.active().count(),
            'closed': user.closed().count(),
            'won': user.won_listings().count(),
            'watched': user.user_watchlist.all().count(),

        }

        context['q_set'] = self.kwargs.get('q_set')
        context['counts'] = counts
        return context 

    def get_queryset(self):
        queryset = super(UserView, self).get_queryset()
        user = self.request.user

        # Since queries don't hit database until evalution, construct dict of options.
        q_sets = {
            'active': user.active(),
            'closed': user.closed(),
            'won': user.won_listings(),
            'watched': user.watched(),
        }
        q = self.kwargs.get('q_set')
        if q:
            return q_sets[q]
        return user.active()


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AuctionUser
    success_url = '/' 


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AuctionUser
    template_name = 'users/edit_profile.html'
    form_class = UserUpdateForm

    def test_func(self):
        # Ensure users can only edit their own profile
        user = self.get_object()
        return self.request.user == user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        counts = {
            'active': user.active().count(),
            'closed': user.closed().count(),
            'won': user.won_listings().count(),
            'watched': user.user_watchlist.all().count(),

        }
        context['counts'] = counts

        return context
    

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