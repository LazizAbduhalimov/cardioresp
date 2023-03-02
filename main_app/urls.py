from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path("favicon.ico", favicon),
    path('authors/', AuthorsPage.as_view(), name="authors"),
    path('authors/<slug:slug>/', AuthorsDetailPage.as_view(), name="author-detail"),
    path('submission/', cache_page(60*15)(SubmissionPage.as_view()), name="submission"),
    path('editorial-office/', EditorialPage.as_view(), name="editorial-team"),
    path('editorial-office/<slug:slug>', EditorialMemberPage.as_view(), name="editorial-member"),
    path('<slug:slug>/', cache_page(60*15)(SamePages.as_view()), name="same-pages"),
]
