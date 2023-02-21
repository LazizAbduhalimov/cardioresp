from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.views.generic import UpdateView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from profiles.forms import ArticleCreateForm
from blogs.utils import ArticleModificationMixin
from main_app.utils import MenuMixin
from .models import AuthorsProfile
from blogs.models import Article, ArticleStatusEnum


class AuthorsProfilePage(LoginRequiredMixin, MenuMixin, DetailView):
    login_url = reverse_lazy("login")
    model = AuthorsProfile
    template_name = "authors_profile/authors_profile.html"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(AuthorsProfilePage, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        author = self.model.objects.get(slug=slug)
        if self.request.user != author.user:
            raise Http404()
        if self.request.GET.get("isSuccessful"):
            messages.add_message(
                self.request, messages.INFO,
                "Статья добавлена в очередь рецензирования. Мы отправим вам уведомление на почту после проверки вашей статьи"
            )
        context["object"] = author
        context["articles"] = Article.objects.filter(authors=author)

        return dict(list(context.items()) + list(self.get_user_context().items()))


class ArticleCreate(LoginRequiredMixin, MenuMixin, CreateView):
    form_class = ArticleCreateForm
    template_name = "authors_profile/article_create.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super(ArticleCreate, self).get_context_data(**kwargs)
        return dict(list(context.items()) + list(self.get_user_context().items()))

    def form_valid(self, form, *args, **kwargs):
        article = form.save()
        # if not article.is_draft:
        #     article.status = "рецензируется"
        article.authors.add(AuthorsProfile.objects.get(user=self.request.user))
        article.save()
        return HttpResponseRedirect("{}?isSuccessful=True".format(reverse_lazy("article-update", kwargs={"slug": article.slug})))


class ArticleUpdate(LoginRequiredMixin, ArticleModificationMixin, MenuMixin, UpdateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = "authors_profile/article_update.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(**kwargs)

        if self.request.GET.get("isSuccessful"):
            messages.add_message(
                self.request, messages.INFO,
                "Для заполнения полей на других языках переключайтесь между языками в правой панеле"
            )

        return dict(list(context.items()) + list(self.get_user_context().items()))

    def form_valid(self, form, *args, **kwargs):
        article = form.save()
        author = AuthorsProfile.objects.get(user=self.request.user)
        params = ""

        if not article.is_draft and (article.status == ArticleStatusEnum.draft.value or
                                     article.status == ArticleStatusEnum.rejected.value):
            article.status = ArticleStatusEnum.reviewing.value
            params = "?isSuccessful=True"

        if article.is_draft:
            article.status = ArticleStatusEnum.draft.value

        article.save()
        return HttpResponseRedirect("{}{}".format(author.get_absolute_url(), params))
