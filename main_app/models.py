from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.safestring import mark_safe
from pytils.translit import slugify


class LinkLocation(models.Model):
    title = models.CharField("Название", max_length=100, default="")

    class Meta:
        verbose_name = "Link Location"
        verbose_name_plural = "Link Locations"

    def __str__(self):
        return f"{self.title} - ID: {self.id}"


class Page(models.Model):
    title = models.CharField("Название страницы", max_length=100)
    content = RichTextField("Содержание", blank=True)
    linklocation = models.ForeignKey(LinkLocation, verbose_name="Link Locations", null=True, on_delete=models.DO_NOTHING)
    slug = models.SlugField("Slug страницы", max_length=200, blank=True, unique=True)

    class Meta:
        verbose_name = "Страницу"
        verbose_name_plural = "Страницы"

    def get_absolute_url(self):
        return reverse('same-pages', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        super(Page, self).save(*args, **kwargs)

    def cut_content(self):

        if self.content:
            return mark_safe(
                f'{self.content[:200]}...'
            )
        else:
            return 'Text Not Found'

    cut_content.short_description = 'Содержание'

    def __str__(self):
        return self.title


class Post(models.Model):
    position = models.IntegerField(default=0)
    title = models.CharField("Должность", max_length=255, default="")

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

        ordering = ["position"]

    def __str__(self):
        return self.title


class EditorialMember(models.Model):
    position = models.IntegerField(default=0)

    full_name = models.CharField("Ф.И.О.", max_length=255, default="")
    location = models.CharField("Место работы", max_length=255, default="")
    post = models.ForeignKey(Post, verbose_name="Занимаемая должность", null=True, on_delete=models.DO_NOTHING)
    about = RichTextField("Об авторе")

    e_mail = models.EmailField(verbose_name="E-mail", max_length=255)

    slug = models.SlugField("Slug страницы", max_length=200, blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super(EditorialMember, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('editorial-member', kwargs={'slug': self.slug})

    def __str__(self):
        return  self.full_name

    class Meta:
        verbose_name = "Участника редакции"
        verbose_name_plural = "Редакция"

        ordering = ["position"]
