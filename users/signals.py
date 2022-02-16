from socket import send_fds
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Create profile instance when user registers for an account.
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Save profile instance when user instance is saved.
    instance.profile.save()