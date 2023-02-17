from django.http import Http404
from blogs.models import *


class ArticleModificationMixin:

    def dispatch(self, request, *args, **kwargs):
        try:
            AuthorsProfile.objects.get(user=request.user)
        except:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)
