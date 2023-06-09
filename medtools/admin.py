from django.contrib import admin
from .models import *

from nested_admin.nested import NestedModelAdmin, NestedTabularInline

class EchocardiographyInline(admin.StackedInline):
    model = Echocardiography
    extra = 0
    max_num = 1


class GeneticResearchInline(admin.StackedInline):
    model = GeneticResearch
    extra = 0
    max_num = 1


class ImmunologicalResearchInline(admin.StackedInline):
    model = ImmunologicalResearch
    extra = 0
    max_num = 1


class PilidogramInline(admin.StackedInline):
    model = Pilidogram
    extra = 0
    max_num = 1


class BodyMassIndexInLine(admin.StackedInline):
    model = BodyMassIndex
    extra = 0
    max_num = 1


class BiochemicalBloodAnalysisInline(admin.StackedInline):
    model = BiochemicalBloodAnalysis
    extra = 0
    max_num = 1


class CoronaryAngiographyInline(admin.StackedInline):
    model = CoronaryAngiography
    extra = 0
    max_num = 1


class ECGInline(admin.StackedInline):
    model = ECG
    extra = 0
    max_num = 1


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


@admin.register(Echocardiography)
class EchocardiographyAdmin(admin.ModelAdmin):
    list_per_page = 15


@admin.register(ImmunologicalResearch)
class ImmunologicalResearchAdmin(admin.ModelAdmin):
    list_per_page = 15


@admin.register(GeneticResearch)
class GeneticResearchAdmin(admin.ModelAdmin):
    list_per_page = 15


class SurveyQuestionChoicesInLine(NestedTabularInline):
    model = SurveyQuestionChoices
    extra = 2


class SurveyQuestionInline(NestedTabularInline):
    model = SurveyQuestion
    extra = 0

    inlines = [SurveyQuestionChoicesInLine]


@admin.register(Survey)
class SurveyAdmin(NestedModelAdmin):
    list_display = [
        "name",
    ]

    inlines = [
        SurveyQuestionInline
    ]

    list_per_page = 15


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "choice",
    ]

    list_per_page = 40


@admin.register(SurveyMultipleAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
    ]

    list_per_page = 40


@admin.register(SurveyResult)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = [
        "survey",
        "text",
    ]

    list_per_page = 40
