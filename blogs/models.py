from enum import Enum

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from pytils.templatetags.pytils_translit import slugify
from django.utils.translation import gettext_lazy as _

import qrcode

from authors_profile.models import AuthorsProfile
from cardioresp.settings import MEDIA_ROOT
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from ckeditor.fields import RichTextField


class ArticleStatusEnum(str, Enum):
    draft = "черновик"
    reviewing = "рецензируется"
    denied = "отклонено"
    accepted = "принят"
    published = "опубликован"


article_status_choices = [
    (ArticleStatusEnum.draft.value, 'Черновик'),
    (ArticleStatusEnum.reviewing.value, 'Рецензируется'),
    (ArticleStatusEnum.denied.value, 'Отклонено'),
    (ArticleStatusEnum.accepted.value, 'Принят'),
    (ArticleStatusEnum.published.value, 'Опубликован'),
]


class State(models.Model):
    title = models.CharField("Название статуса", max_length=150)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Tags(models.Model):
    title = models.CharField("Ключевое слово", max_length=150)
    related_articles_number = models.IntegerField("Количество связанных статей", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"

        ordering = ["title"]


class Volume(models.Model):
    title = models.CharField("Название тома", max_length=255, default="")
    doi = models.CharField("DOI ссылка", max_length=255, default="")
    file = models.FileField("Файл (PDF)", upload_to="files/Volume/", blank=True, null=True)
    published_date = models.DateField("Дата публикации", default=now, editable=True)
    qr = models.ImageField("QR-код", upload_to="images/volumes/QR/", blank=True)

    slug = models.SlugField("Slug тома", max_length=200, blank=True, null=True)
    status = models.ForeignKey(State, verbose_name="Статус", on_delete=models.DO_NOTHING)
    status_str = models.CharField("Строка статуса", blank=True, max_length=100)

    def get_absolute_url(self):
        return reverse('issue-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.status_str = str(self.status)
        self.slug = slugify(self.title)

        # Создание и сохранение qr-code
        url = MEDIA_ROOT.replace("\\", "/") + "/" + str(self.file)
        qrcode_image = qrcode.make(url)
        canvas = Image.new("RGB", (qrcode_image.pixel_size, qrcode_image.pixel_size), "white")
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        file_name = f"qrcode-{self.title}.png"
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        self.qr.save(file_name, File(buffer), save=False)
        canvas.close()

        # При статусе Неактивынй отключаем все связанные Статьи, а иначе включаем их
        if self.status_str == "Неактивный" or self.status_str == "Следующий":
            if self.status_str == "Следующий":
                for i in Volume.objects.exclude(title=self.title).filter(status_str="Следующий"):
                    i.status = State.objects.get(title="Активный")
                    i.save()

            for i in Article.objects.filter(linked_volume=self):
                i.is_active = False
                i.save()
        else:
            for i in Article.objects.filter(linked_volume=self):
                i.is_active = True
                i.save()

        # Если модель получит статус Активный то другая модель с таким же статусом станет Архивной
        if self.status_str == "Активный":

            for i in Volume.objects.exclude(title=self.title).filter(status_str="Активный"):
                i.status = State.objects.get(title="Архивный")
                i.save()

        super(Volume, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def admin_image(self):

        if self.qr:
            return mark_safe(
                u'<a href="{0}" target="_blank"><img src="{0}" width="100" /></a>'.format(self.qr.url))
        else:
            return 'Image Not Found'

    admin_image.short_description = 'QR-код'
    admin_image.allow_tags = True

    class Meta:
        verbose_name = "Том"
        verbose_name_plural = "Тома"
        ordering = ["-published_date"]


class ArticleSection(models.Model):
    position = models.IntegerField(default=0)
    title = models.CharField("Название раздела", max_length=255, default="")

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы статьи"

        ordering = ["position"]

    def __str__(self):
        return self.title


class UniqueViewers(models.Model):
    user_id = models.CharField("ID", max_length=255)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = "Уникального пользователя"
        verbose_name_plural = "Уникальные пользователи"


class Article(models.Model):
    position = models.IntegerField(default=0)

    title = models.CharField(_("Заголовок статьи"), max_length=255, default="")
    slug = models.SlugField(_("Slug статьи"), max_length=200, blank=True)
    annotation = RichTextField(_("Аннотация"), default="")
    for_quoting = models.TextField(_("Для цитирования"), default="", blank=True, null=True)

    doi = models.CharField(_("DOI ссылка"), max_length=255, default="", null=True)
    file = models.FileField(_("Файл (PDF)"), upload_to="files/Article/", null=True)

    linked_volume = models.ForeignKey(Volume, verbose_name=_("Связанный том"), null=True, on_delete=models.DO_NOTHING)
    chapter = models.ForeignKey(ArticleSection, verbose_name=_("Раздел"), null=True, on_delete=models.DO_NOTHING)
    authors = models.ManyToManyField(AuthorsProfile, verbose_name=_("Связанные Авторы"), related_name='authors', blank=True)
    authors_text = models.CharField(_("Авторы (Текст)"), max_length=255, default="")
    tags = models.ManyToManyField(Tags, verbose_name=_("Ключевые слова"), related_name='tags', blank=True)
    created_date = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_date = models.DateTimeField(_("Дата последнего изменения"), auto_now=True)
    published_date = models.DateField(_("Дата публикации"), default=now, editable=True)
    status = models.CharField(_("Статус"), max_length=100, default=ArticleStatusEnum.draft, choices=article_status_choices)
    is_draft = models.BooleanField(_("Черновик"), default=True)

    viewers = models.ManyToManyField(UniqueViewers, verbose_name=_("Просмотры"), related_name="viewers")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('article-update', kwargs={'slug': self.slug})

    def cut_title(self):

        if self.title:
            from django.utils.safestring import mark_safe
            return mark_safe(
                f'{self.title[:50]}...'
            )
        else:
            return 'Text Not Found'

    cut_title.short_description = 'Аннотация'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статью"
        verbose_name_plural = "Статьи"

        ordering = ["published_date", "title"]
