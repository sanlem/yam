from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import Profile


@receiver(post_save, sender=User, dispatch_uuid="user_saved")
def create_profile(sender, **kwargs):
    print("Inited")
    if isinstance(sender, User):
        if kwargs["created"] is True:
            user = kwargs["instance"]
            # new user is created, lets add profile for it
            p = Profile()
            p.save()
            p.user = user
            p.save()
