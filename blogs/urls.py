from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('tag-cloud/', TagCloudPage.as_view(), name="tag-cloud"),
    path('issue/', ArchiveView.as_view(), name="issue"),
    path('issue/<slug:slug>/', IssueDetail.as_view(), name="issue-detail"),
    path('issue/article/<slug:slug>/', ArticleView.as_view(), name="article"),
    path("pdf/article/<slug:slug>.pdf", PdfView.as_view(), name="pdf-view"),
    path("pdf/volume/<slug:slug>", PdfViewVolume.as_view(), name="pdf-view-volume"),
]
