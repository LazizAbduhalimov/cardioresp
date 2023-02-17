from django.urls import path
from .views import *


urlpatterns = [
    path('author-profile/<slug:slug>', AuthorsProfilePage.as_view(), name="author-profile"),
]
