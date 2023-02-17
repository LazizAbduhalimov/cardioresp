from blogs.models import *
from main_app.models import *


class MenuMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context["links"] = Page.objects.filter(linklocation__title="About us")
        context["menu_links"] = Page.objects.filter(linklocation__title="Menu")
        try:
            context["author_profile"] = AuthorsProfile.objects.filter(user=self.request.user).first()
        except TypeError:
            context["author_profile"] = None
        context["is_authorized"] = bool(context["author_profile"])

        context["side_bar_links"] = Page.objects.filter(linklocation__title="Side bar")
        try:
            context["next_volume"] = Volume.objects.filter(status_str="Следующий")[0]
        except IndexError:
            context["next_volume"] = None
        context["current_path"] = str(self.request.path)[3:]
        return context
