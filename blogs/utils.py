from django.http import Http404
from blogs.models import *


class ArticleModificationMixin:

    def dispatch(self, request, *args, **kwargs):
        try:
            author = AuthorsProfile.objects.get(user=request.user)
            article = Article.objects.get(slug=kwargs["slug"], authors=author)
        except:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)
