from django.contrib import admin

from .models import *
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Volume)
class AdminVolume(TabbedTranslationAdmin):
    list_display = [
        "title",
        "get_doi_color",
        "admin_image",
        "slug",
        "get_status_color",
    ]
    readonly_fields = ["slug"]
    exclude = ["qr"]

    def get_doi_color(self, object):
        return mark_safe(f"<span style='color: DarkGray;'><italic>{object.doi}</italic></span>")

    def get_status_color(self, object):
        if str(object.status) == "Неактивный":
            print("!")
            return mark_safe(f"<span style='color: red'><strong>{object.status}</strong></span>")
        elif str(object.status) == "Активный":
            return mark_safe(f"<span style='color: Lime'><strong>{object.status}</strong></span>")
        elif str(object.status) == "Архивный":
            return mark_safe(f"<span style='color: DodgerBlue'><strong>{object.status}</strong></span>")
        elif str(object.status) == "Следующий":
            return mark_safe(f"<span style='color: DarkOrange'><strong>{object.status}</strong></span>")
        else:
            return object.status

    list_per_page = 15


@admin.register(Tags)
class AdminTags(TabbedTranslationAdmin):
    list_display = [
        "title",
        "related_articles_number"
    ]
    readonly_fields = ["related_articles_number"]
    list_per_page = 50


@admin.register(ArticleSection)
class AdminArticleSection(TabbedTranslationAdmin):
    list_display = ["title", "position"]
    list_editable = ["position"]
    list_per_page = 50


@admin.register(Article)
class AdminArticle(TabbedTranslationAdmin):
    list_display = [
        "cut_title",
        "doi",
        "published_date",
        "slug"
    ]
    filter_horizontal = ["authors", ]
    prepopulated_fields = {"slug": ("title",)}
    exclude = ["viewers"]
    readonly_fields = ["created_date", "updated_date"]

    list_filter = ["linked_volume", "chapter"]
    list_per_page = 15


@admin.register(UniqueViewers)
class AdminPartner(admin.ModelAdmin):
    list_display = [
        "user_id",
    ]
    list_per_page = 50


@admin.register(Comment)
class AdminPartner(admin.ModelAdmin):
    list_display = [
        "reviewer",
        "article",
    ]
    list_per_page = 50