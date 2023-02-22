from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import AuthorsProfile, ReviewersProfile
from pytils.templatetags.pytils_translit import slugify


@receiver(pre_save, sender=AuthorsProfile)
def calc_ac_total(sender, instance, **kwargs):
    if instance.full_name == "":
        instance.full_name = instance.user.get_full_name()
    if instance.slug == "":
        instance.slug = slugify(instance.full_name)


@receiver(pre_save, sender=ReviewersProfile)
def calc_ac_total(sender, instance, **kwargs):
    if instance.full_name == "":
        instance.full_name = instance.user.get_full_name()
    if instance.slug == "":
        instance.slug = slugify(instance.full_name)
