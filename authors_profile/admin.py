from django.contrib import admin

from .models import *


@admin.register(AuthorsProfile)
class AdminState(admin.ModelAdmin):
    list_display = [
        "user",
    ]
    list_per_page = 15