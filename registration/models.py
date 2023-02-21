from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField


class User(AbstractUser):
    middle_name = models.CharField(_("Отчество"), max_length=255, default="")
    post = models.CharField(_("Должность"), max_length=255, default="")
    workplace = models.CharField(_("Место работы"), max_length=255, default="")
    orcid = models.CharField(_("ORCHID"), max_length=255, default="")
    country = CountryField(verbose_name=_("Страна"), default="")
