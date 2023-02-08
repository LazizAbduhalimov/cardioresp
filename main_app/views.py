from django.http import HttpResponseRedirect, FileResponse, HttpRequest
from django.views.generic import ListView, DetailView
from blogs.models import Volume, Article, Tags, Authors, ArticleSection
from main_app.models import *
from main_app.utils import MenuMixin
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)
def favicon(request: HttpRequest):
    file = (settings.BASE_DIR / "static" / "favicon.ico").open("rb")
    return FileResponse(file)


def index(request):
    return HttpResponseRedirect("ru/home/")


class SamePages(MenuMixin, DetailView):
    model = Page
    template_name = "main_app/same_pages.html"
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(SamePages, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context["object"] = Page.objects.get(slug=slug)

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class SubmissionPage(MenuMixin, ListView):
    model = Page
    template_name = "main_app/submission.html"

    def get_context_data(self, **kwargs):
        context = super(SubmissionPage, self).get_context_data(**kwargs)
        context["object"] = self.model.objects.get(slug="submission")

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class Search(MenuMixin, ListView):
    template_name = "main_app/search.html"
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get("q") != "" and 'tag' not in self.request.GET:
            queryset = Article.objects.filter(is_active=True).filter(
                title__icontains=self.request.GET.get("q"))
            return queryset.distinct()

        queryset = Article.objects.filter(is_active=True)
        tags = self.request.GET.getlist("tag")
        print(self.request.GET.getlist("tag"))
        for tag in tags:
            queryset = queryset.filter(tags=tag)

        if self.request.GET.get("q") != "" and 'tag' in self.request.GET:
            queryset = queryset.filter(title__icontains=self.request.GET.get("q"))

        # distinct чтобы не было дубликаций модели
        return queryset.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.GET.get("q"):
            context["q"] = self.request.GET.get("q")
        else:
            context["q"] = ""

        for tag in Tags.objects.all():
            related_articles = Article.objects.filter(tags=tag)
            tag.related_articles_number = related_articles.count()
            tag.save()

        context["filter_tags"] = self.request.GET.getlist("tag")
        context["tags"] = Tags.objects.order_by("-related_articles_number")

        context["current_path"] = f"{str(self.request.path)[3:]}?q="
        return dict(list(context.items()) + list(self.get_user_context().items()))


class EditorialPage(MenuMixin, ListView):
    model = EditorialMember
    template_name = "main_app/editorial_page.html"

    def get_context_data(self, **kwargs):
        context = super(EditorialPage, self).get_context_data(**kwargs)
        context["posts"] = Post.objects.all()
        context["members"] = EditorialMember.objects.all()

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class EditorialMemberPage(MenuMixin, DetailView):
    model = EditorialMember
    template_name = "main_app/editorial_member_page.html"
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(EditorialMemberPage, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context["object"] = self.model.objects.get(slug=slug)

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class AuthorsPage(MenuMixin, ListView):
    model = Authors
    template_name = "main_app/authors.html"
    paginate_by = 10

    def get_queryset(self):
        if "/ru/" in self.request.path:
            queryset = self.model.objects.order_by("name_ru")
        else:
            queryset = self.model.objects.order_by("name_en")

        return queryset

    def get_context_data(self, **kwargs):
        context = super(AuthorsPage, self).get_context_data(**kwargs)

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))


class AuthorsDetailPage(MenuMixin, DetailView):
    model = Authors
    template_name = "main_app/author's_articles.html"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(AuthorsDetailPage, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context["authors"] = self.model.objects.all()
        context["article_section"] = ArticleSection.objects.all()
        context["articles"] = Article.objects.filter(authors=self.model.objects.get(slug=slug)).distinct()

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))