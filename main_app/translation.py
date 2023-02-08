from modeltranslation.translator import register, TranslationOptions
from .models import Page, Post, EditorialMember


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ("title", "content")


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(EditorialMember)
class EditorialMemberTranslationOptions(TranslationOptions):
    fields = (
        "full_name",
        "location",
        "about",
    )
