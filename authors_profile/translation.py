from modeltranslation.translator import register, TranslationOptions
from .models import AuthorsProfile


@register(AuthorsProfile)
class AuthorsProfileTranslationOptions(TranslationOptions):
    fields = ("full_name",)

