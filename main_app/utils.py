from django.views import View

from blogs.models import *
from main_app.models import *
from medtools.models import Patient
from profiles.models import AuthorsProfile


def get_or_none(class_model, **kwargs):
    try:
        return class_model.objects.get(**kwargs)
    except class_model.DoesNotExist:
        return None


class MenuMixin(View):

    def get_user_context(self, **kwargs):
        context = kwargs
        all_pages = Page.objects.all()
        context["links"] = all_pages.filter(linklocation__title="About us").select_related("linklocation")
        context["menu_links"] = all_pages.filter(linklocation__title="Menu").select_related("linklocation")
        context["side_bar_links"] = all_pages.filter(linklocation__title="Side bar").select_related("linklocation")

        context["next_volume"] = get_or_none(Volume, status="Следующий")
        context["current_path"] = str(self.request.path)[3:]

        patient_id = self.request.session.get("patient_id", None)
        patient = get_or_none(Patient, pk=patient_id)
        if patient is None:
            self.request.session["patient_id"] = None
        context["patient_id"] = self.request.session.get("patient_id", None)

        if self.request.user.is_authenticated:
            context["author_profile"] = get_or_none(AuthorsProfile, user=self.request.user)
            context["is_author"] = bool(context["author_profile"])

            context["reviewer_profile"] = get_or_none(ReviewersProfile, user=self.request.user)
            context["is_reviewer"] = bool(context["reviewer_profile"])

        return context
