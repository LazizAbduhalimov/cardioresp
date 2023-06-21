from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .inlines import *
from nested_admin.nested import NestedModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]

    inlines = [
        EchocardiographyInline, GeneticResearchInline, ImmunologicalResearchInline,
        PilidogramInline, BodyMassIndexInLine, BiochemicalBloodAnalysisInline, CoronaryAngiographyInline, ECGInline
    ]

    list_per_page = 15


class SurveyResource(resources.ModelResource):
    class Meta:
        model = Survey


class SurveyQuestionResource(resources.ModelResource):
    class Meta:
        model = SurveyQuestion


class SurveyResultResource(resources.ModelResource):
    class Meta:
        model = SurveyResult


class SurveyAnswerChoicesResource(resources.ModelResource):
    class Meta:
        model = SurveyQuestionChoices


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    inlines = [SurveyQuestionChoicesInLine]
    resource_classes = [SurveyQuestionResource]
    list_per_page = 30


@admin.register(SurveyQuestionChoices)
class SurveyQuestionChoicesAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    resource_classes = [SurveyAnswerChoicesResource]
    list_per_page = 30


@admin.register(Survey)
class SurveyAdmin(NestedModelAdmin, ImportExportModelAdmin, TabbedTranslationAdmin):
    resource_classes = [SurveyResource]
    list_display = [
        "name",
    ]

    inlines = [
        SurveyQuestionInline
    ]

    list_per_page = 15


@admin.register(SurveyResult)
class SurveyResultAdmin(ImportExportModelAdmin, TabbedTranslationAdmin):
    resource_classes = [SurveyResultResource]
    list_display = [
        "survey",
        "text",
    ]

    list_per_page = 40
