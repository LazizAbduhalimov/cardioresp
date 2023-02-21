from django.db.models.signals import post_delete, post_migrate
from django.dispatch import receiver
from .models import LinkLocation

__default_linklocation_objects = ("Hidden", "About us", "Side bar", "Menu")


@receiver((post_delete, post_migrate), sender=LinkLocation)
def create_default_objects(sender, **kwargs):
    for obj in __default_linklocation_objects:

        links = sender.objects.filter(title=obj)
        if len(links) < 1:
            new_link = sender(title=obj)
            new_link.save()
