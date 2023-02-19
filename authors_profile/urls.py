from django.urls import path
from .views import *


urlpatterns = [
    path('author-profile/<slug:slug>', AuthorsProfilePage.as_view(), name="author-profile"),
    path('article/create/', ArticleCreate.as_view(), name="article-create"),
    path('article/update/<slug:slug>', ArticleUpdate.as_view(), name="article-update"),
]
