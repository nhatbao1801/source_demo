#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH

import cloudinary.api
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from event.models.event import Event
from event.models.media import Media


@receiver(pre_delete, sender=Event)
def delete_profile_and_cover_picture(sender, **kwargs):
    instance = kwargs.get('instance')
    try:
        # Delete profile picture of the event
        if instance.picture is not None:
            cloudinary.api.delete_resources(instance.picture.public_id)
        # Delete cover picture of the event
        media = Media.objects.get(Q(event_id=instance.id) & Q(set_as_cover=True))
        # Delete resource image
        if media.image is not None:
            cloudinary.api.delete_resources(media.image.public_id)
    except (Media.DoesNotExist, Exception) as e:
        pass
