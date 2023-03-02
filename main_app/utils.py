from blogs.models import *
from main_app.models import *
from profiles.models import AuthorsProfile


class MenuMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        all_pages = Page.objects.all()
        context["links"] = all_pages.filter(linklocation__title="About us").select_related("linklocation")
        context["menu_links"] = all_pages.filter(linklocation__title="Menu").select_related("linklocation")
        context["side_bar_links"] = all_pages.filter(linklocation__title="Side bar").select_related("linklocation")
        try:
            context["author_profile"] = AuthorsProfile.objects.filter(user=self.request.user).first()
        except TypeError:
            context["author_profile"] = None
        context["is_author"] = bool(context["author_profile"])

        try:
            context["reviewer_profile"] = ReviewersProfile.objects.filter(user=self.request.user).first()
        except TypeError:
            context["reviewer_profile"] = None
        context["is_reviewer"] = bool(context["reviewer_profile"])

        try:
            context["next_volume"] = Volume.objects.filter(status="Следующий").first()
        except TypeError:
            context["next_volume"] = None
        context["current_path"] = str(self.request.path)[3:]
        return context
