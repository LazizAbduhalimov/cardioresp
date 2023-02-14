from django.db import models
from django.urls import reverse
from pytils.templatetags.pytils_translit import slugify

from registration.models import User


class AuthorsProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="Зарегестрированный пользователь", related_name="user", on_delete=models.DO_NOTHING)
    slug = models.SlugField("Slug статьи", max_length=200, blank=True)

    def save(self, *args, ** kwargs):
        if self.slug == "":
            self.slug = slugify(self.user)
        super().save(self, *args, *kwargs)

    def get_absolute_url(self):
        return reverse('author-profile', kwargs={'slug': self.slug})

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Автора"
        verbose_name_plural = "Авторы"
