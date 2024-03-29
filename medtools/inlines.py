from django.contrib import admin
from modeltranslation.admin import TranslationTabularInline

from nested_admin.nested import NestedTabularInline

from .models import *


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
    model = Lipidogram
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


class SurveyQuestionChoicesInLine(NestedTabularInline):
    model = SurveyQuestionChoices
    extra = 0


class SurveyQuestionInline(NestedTabularInline, TranslationTabularInline):
    model = SurveyQuestion
    extra = 0

    inlines = [SurveyQuestionChoicesInLine]