from django.db import models
from django.urls import reverse

from registration.models import User


class AuthorsProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="Зарегестрированный пользователь", related_name="author_user", on_delete=models.DO_NOTHING)
    full_name = models.CharField("Имя, Фамилия", max_length=255, default="", blank=True)
    slug = models.SlugField("Slug статьи", max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('author-profile', kwargs={'slug': self.slug})

    def get_url_for_viewers(self):
        return reverse("author-detail", kwargs={'slug': self.slug})

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Автора"
        verbose_name_plural = "Авторы"


class ReviewersProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="Зарегестрированный пользователь", related_name="reviewer_user", on_delete=models.DO_NOTHING)
    full_name = models.CharField("Имя, Фамилия", max_length=255, default="", blank=True)
    slug = models.SlugField("Slug статьи", max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('reviewer-profile', kwargs={'slug': self.slug})

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Рецензента"
        verbose_name_plural = "Рецензенты"