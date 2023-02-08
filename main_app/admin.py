from django.contrib import admin
from main_app.models import *
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Page)
class AdminPage(TabbedTranslationAdmin):
    list_display = [
        "title",
        "cut_content",
        "linklocation",
        "slug"
    ]

    list_per_page = 15


@admin.register(LinkLocation)
class AdminLinkLocation(admin.ModelAdmin):
    list_display = [
        "title",
    ]

    list_per_page = 15


@admin.register(Post)
class AdminPost(TabbedTranslationAdmin):
    list_display = [
        "title",
        "position",
    ]
    list_editable = ["position"]
    list_per_page = 15


@admin.register(EditorialMember)
class AdminEditorialMember(TabbedTranslationAdmin):
    list_display = [
        "full_name",
        "location",
        "slug",
        "position",
    ]
    list_editable = ["position"]
    readonly_fields = ["slug"]
    list_per_page = 15