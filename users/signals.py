from django.db.models.signals import post_save #signal fired after an object is saved
from django.contrib.auth.models import User # sender of the signal
from django.dispatch import receiver  # signal receiver
from .models import Profile

@receiver(post_save, sender=User) #receiver is decorator
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User) #receiver is decorator
def save_profile(sender, instance, **kwargs):
    instance.profile.save()



''' when user is saved send signal
signal is received by receiver
receiver is create_profile function

'''


