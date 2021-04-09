from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Profile


def profile_creation(sender, instance, created, **kwargs):
    '''
    used as signal,
    fires up when the user is created
    '''
    if created:
        '''
        whenever an new user is created, the user will be added to the user-group
        '''
        group = Group.objects.get(name='user-group')
        instance.groups.add(group)
        Profile.objects.create(
            user=instance,
        )
        # Profile Created


post_save.connect(profile_creation, sender=User)
