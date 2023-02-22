from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import *


@admin.register(AuthorsProfile)
class AdminState(TabbedTranslationAdmin):
    list_display = [
        "user",
    ]
    list_per_page = 15


@admin.register(ReviewersProfile)
class AdminState(TabbedTranslationAdmin):
    list_display = [
        "user",
    ]
    list_per_page = 15