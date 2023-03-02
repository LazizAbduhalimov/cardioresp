from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.views.generic import UpdateView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from profiles.forms import ArticleCreateForm, CommentCreateForm
from blogs.utils import ArticleModificationMixin
from main_app.utils import MenuMixin
from .models import AuthorsProfile, ReviewersProfile
from blogs.models import Article, ArticleStatusEnum, Comment


class AuthorsProfilePage(LoginRequiredMixin, MenuMixin, DetailView):
    login_url = reverse_lazy("login")
    model = AuthorsProfile
    template_name = "profiles/authors_profile.html"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(AuthorsProfilePage, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        author = self.object
        if self.request.user != author.user:
            raise Http404()
        context["articles"] = Article.objects.filter(authors=author)

        return dict(list(context.items()) + list(self.get_user_context().items()))


class ArticleCreate(LoginRequiredMixin, MenuMixin, CreateView):
    form_class = ArticleCreateForm
    template_name = "profiles/article_create.html"
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
        messages.add_message(
            self.request, messages.INFO,
            "Для заполнения полей на других языках переключайтесь между языками в правой панеле"
        )
        return HttpResponseRedirect(reverse_lazy("article-update", kwargs={"slug": article.slug}))


class ArticleUpdate(LoginRequiredMixin, ArticleModificationMixin, MenuMixin, UpdateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = "profiles/article_update.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(**kwargs)
        article = self.object
        context["comments"] = Comment.objects.filter(article=article).select_related("reviewer")\
            .only("text", "reviewer__full_name")
        return dict(list(context.items()) + list(self.get_user_context().items()))

    def form_valid(self, form, *args, **kwargs):
        article = form.save()
        article.authors.add(AuthorsProfile.objects.get(user=self.request.user))
        author = AuthorsProfile.objects.get(user=self.request.user)
        params = ""

        if not article.is_draft and (article.status == ArticleStatusEnum.draft.value or
                                     article.status == ArticleStatusEnum.rejected.value):
            article.status = ArticleStatusEnum.reviewing.value
            messages.add_message(
                self.request, messages.INFO,
                "Статья добавлена в очередь рецензирования. Мы отправим вам уведомление на почту после проверки вашей статьи"
            )
        if article.is_draft:
            messages.add_message(
                self.request, messages.INFO,
                "Статья успешно добавлена в черновики"
            )
            article.status = ArticleStatusEnum.draft.value
        article.save()
        return HttpResponseRedirect(author.get_absolute_url())


class ReviewersProfilePage(LoginRequiredMixin, MenuMixin, DetailView):
    login_url = reverse_lazy("login")
    model = ReviewersProfile
    template_name = "profiles/reviewer_profile.html"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(ReviewersProfilePage, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        reviewer = self.model.objects.get(slug=slug)
        if self.request.user != reviewer.user:
            raise Http404()
        context["object"] = reviewer
        context["articles"] = Article.objects.filter(is_draft=False, status=ArticleStatusEnum.reviewing.value).exclude(
            comment_article__reviewer=reviewer).distinct()
        context["comments"] = Comment.objects.filter(reviewer=reviewer).exclude(
            article__is_draft=True, article__status=ArticleStatusEnum.draft.value).distinct()

        return dict(list(context.items()) + list(self.get_user_context().items()))


class ArticleReviewing(MenuMixin, CreateView):
    form_class = CommentCreateForm
    template_name = "profiles/article_reviewing.html"
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ArticleReviewing, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        if Article.objects.get(slug=slug).is_draft:
            raise Http404()

        context["object"] = Article.objects.get(slug=slug)

        return dict(list(context.items()) + list(self.get_user_context().items()))

    def form_valid(self, form, *args, **kwargs):
        comment = form.save(commit=False)
        comment.article = Article.objects.get(slug=self.kwargs["slug"])
        reviewer = ReviewersProfile.objects.get(user=self.request.user)
        comment.reviewer = reviewer
        comment.save()
        messages.add_message(
            self.request, messages.INFO,
            "Ваша рецензия была принята!"
        )
        return HttpResponseRedirect(reverse_lazy("reviewer-profile", kwargs={"slug": reviewer.slug}))


class ArticleUpdatingReview(LoginRequiredMixin, MenuMixin, UpdateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = "profiles/article_update_review.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdatingReview, self).get_context_data(**kwargs)
        slug = self.kwargs["slug"]
        reviewer = ReviewersProfile.objects.get(user=self.request.user)
        comment = Comment.objects.get(slug=slug)
        context["object"] = Article.objects.get(comment_article=comment)
        # if self.request.GET.get("isSuccessful"):
        #     messages.add_message(
        #         self.request, messages.INFO,
        #         "Для заполнения полей на других языках переключайтесь между языками в правой панеле"
        #     )
        return dict(list(context.items()) + list(self.get_user_context().items()))

    def form_valid(self, form, *args, **kwargs):
        comment = form.save()
        reviewer = ReviewersProfile.objects.get(user=self.request.user)
        comment.save()
        messages.add_message(
            self.request, messages.INFO,
            "Ваша рецензия успешно изменена!")
        return HttpResponseRedirect(reviewer.get_absolute_url())
