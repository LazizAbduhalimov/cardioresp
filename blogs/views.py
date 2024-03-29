from django.http import FileResponse, Http404
from django.views.generic import ListView, DetailView

from main_app.utils import MenuMixin
from blogs.models import *


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('HTTP_USER_AGENT')  # В REMOTE_ADDR значение айпи пользователя
    return ip


class ArticleView(MenuMixin, DetailView):
    model = Article
    template_name = "blogs/article.html"
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        if self.object.is_draft:
            raise Http404()

        ip = get_client_ip(self.request)
        user_id = ip
        if not UniqueViewers.objects.filter(user_id=user_id).exists():
            user = UniqueViewers()
            user.user_id = user_id
            user.save()

        viewer = UniqueViewers.objects.get(user_id=user_id)
        article = self.object
        if viewer not in article.viewers.all():
            article.viewers.add(viewer)

        context["authors"] = self.object.authors.all()
        context["published_date"] = self.object.published_date.strftime("%Y/%m/%d")

        return dict(list(context.items()) + list(self.get_user_context().items()))


class ArchiveView(MenuMixin, ListView):
    model = Volume
    template_name = "blogs/archives.html"
    queryset = model.objects.filter(status=VolumeStatusEnum.archive.value)

    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)

        context["current_volume"] = Volume.objects.filter(status=VolumeStatusEnum.active.value)[0]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class IssueDetail(MenuMixin, DetailView):
    model = Volume
    template_name = "blogs/issue.html"
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        articles = Article.objects.filter(
            is_draft=False, status=ArticleStatusEnum.published.value,
            linked_volume=self.model.objects.filter(slug=slug)[0].id).select_related("chapter", ).\
            prefetch_related("authors")
        context["articles"] = articles
        a = set(map(lambda x: x.chapter, articles))
        context["article_section"] = ArticleSection.objects.filter(title__in=list(a))
        return dict(list(context.items()) + list(self.get_user_context().items()))


class TagCloudPage(MenuMixin, ListView):
    model = Tags
    template_name = "blogs/tag_cloud_page.html"
    queryset = model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TagCloudPage, self).get_context_data(**kwargs)
        context["tags"] = Tags.objects.order_by("-related_articles_number")

        return dict(list(context.items()) + list(self.get_user_context().items()))


class PdfView(DetailView):
    slug_field = "slug"

    def get(self, *args, **kwargs):
        try:
            a = Article.objects.get(slug=self.kwargs["slug"])
            return FileResponse(open(MEDIA_ROOT.replace("\\", "/") + "/" + str(a.file), 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()


class PdfViewVolume(DetailView):
    slug_field = "slug"

    def get(self, *args, **kwargs):
        try:
            a = Volume.objects.get(slug=self.kwargs["slug"])
            return FileResponse(open(MEDIA_ROOT.replace("\\", "/") + "/" + str(a.file), 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()


