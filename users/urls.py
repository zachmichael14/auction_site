from django.contrib.auth import views as auth_views
from django.urls import path

from users import views as user_views

app_name = 'users'

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', user_views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', user_views.UserUpdateView.as_view(), name="edit"),
    path('profile/q=<q_set>/', user_views.ProfileView.as_view(), name='profile'),
    ]
