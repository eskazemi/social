from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save




def create_profile(sender, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"])



post_save.connect(sender=User, receiver=create_profile)
