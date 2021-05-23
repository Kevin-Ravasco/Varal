from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save

from .models import Profile
User = get_user_model()


def create_profile_on_user_creation(sender, instance, created, *args, **kwargs):
    # create user profile if the profile is not there as in case of signing in with google.
    if created and not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance)


post_save.connect(create_profile_on_user_creation, sender=User)