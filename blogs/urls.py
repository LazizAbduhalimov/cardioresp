from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('tag-cloud/', TagCloudPage.as_view(), name="tag-cloud"),
    path('issue/', cache_page(60)(ArchiveView.as_view()), name="issue"),
    path('issue/<slug:slug>/', cache_page(60)(IssueDetail.as_view()), name="issue-detail"),
    path('issue/article/<slug:slug>/', cache_page(60*2)(ArticleView.as_view()), name="article"),
    path("pdf/article/<slug:slug>.pdf", PdfView.as_view(), name="pdf-view"),
    path("pdf/volume/<slug:slug>", PdfViewVolume.as_view(), name="pdf-view-volume"),
]
