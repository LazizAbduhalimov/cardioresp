from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView
from django.urls import reverse_lazy

from main_app.utils import MenuMixin
from .models import AuthorsProfile


class AuthorsPage(LoginRequiredMixin, MenuMixin, DetailView):
    login_url = reverse_lazy("login")
    model = AuthorsProfile
    template_name = "authors_profile/authors_profile.html"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(AuthorsPage, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context["object"] = self.model.objects.get(slug=slug)

        context["current_path"] = str(self.request.path)[3:]
        return dict(list(context.items()) + list(self.get_user_context().items()))

