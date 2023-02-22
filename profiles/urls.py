from django.urls import path
from .views import *


urlpatterns = [
    path('reviewer-profile/<slug:slug>', ReviewersProfilePage.as_view(), name="reviewer-profile"),
    path('review/article/<slug:slug>', ArticleReviewing.as_view(), name="article-review"),
    path('update-review/article/<slug:slug>', ArticleUpdatingReview.as_view(), name="article-update-review"),

    path('author-profile/<slug:slug>', AuthorsProfilePage.as_view(), name="author-profile"),
    path('article/create/', ArticleCreate.as_view(), name="article-create"),
    path('article/update/<slug:slug>', ArticleUpdate.as_view(), name="article-update"),
]
