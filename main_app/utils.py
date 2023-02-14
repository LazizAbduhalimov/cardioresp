from blogs.models import *
from main_app.models import *


class MenuMixin:

    def get_user_context(self, **kwargs):
        #context[""]
        context = kwargs
        context["links"] = Page.objects.filter(linklocation__title="About us")
        context["menu_links"] = Page.objects.filter(linklocation__title="Menu")

        context["side_bar_links"] = Page.objects.filter(linklocation__title="Side bar")
        try:
            context["next_volume"] = Volume.objects.filter(status_str="Следующий")[0]
        except:
            context["next_volume"] = None

        return context
