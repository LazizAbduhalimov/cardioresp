from modeltranslation.translator import register, TranslationOptions
from .models import Survey, SurveyResult, SurveyQuestion, SurveyQuestionChoices


@register(Survey)
class AuthorsTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(SurveyResult)
class VolumeTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(SurveyQuestion)
class ArticleTranslationOptions(TranslationOptions):
    fields = ("question",)


@register(SurveyQuestionChoices)
class AuthorsTranslationOptions(TranslationOptions):
    fields = ("choice_text",)