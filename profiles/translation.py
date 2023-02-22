from modeltranslation.translator import register, TranslationOptions
from .models import AuthorsProfile, ReviewersProfile


@register(AuthorsProfile)
class AuthorsProfileTranslationOptions(TranslationOptions):
    fields = ("full_name",)


@register(ReviewersProfile)
class AuthorsProfileTranslationOptions(TranslationOptions):
    fields = ("full_name",)

