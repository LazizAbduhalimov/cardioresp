from django.contrib import admin
from .models import *


class EchocardiographyInline(admin.TabularInline):
    model = Echocardiography
    extra = 0
    max_num = 1


class GeneticResearchInline(admin.TabularInline):
    model = GeneticResearch
    extra = 0
    max_num = 1


class ImmunologicalResearchInline(admin.TabularInline):
    model = ImmunologicalResearch
    extra = 0
    max_num = 1


class PilidogramInline(admin.TabularInline):
    model = Pilidogram
    extra = 0
    max_num = 1


class BodyMassIndexInLine(admin.TabularInline):
    model = BodyMassIndex
    extra = 0
    max_num = 1


class BiochemicalBloodAnalysisInline(admin.TabularInline):
    model = BiochemicalBloodAnalysis
    extra = 0
    max_num = 1


class CoronaryAngiographyInline(admin.TabularInline):
    model = CoronaryAngiography
    extra = 0
    max_num = 1


class ECGInline(admin.TabularInline):
    model = ECG
    extra = 0
    max_num = 1


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
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