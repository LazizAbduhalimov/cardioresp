from django.views.generic import ListView, DetailView, FormView
from extra_views import UpdateWithInlinesView, CreateWithInlinesView, NamedFormsetsMixin

from main_app.utils import MenuMixin
from medtools.forms import *
from medtools.models import Patient


class HeartDiseaseToolPage(NamedFormsetsMixin, MenuMixin, CreateWithInlinesView):
    model = Patient
    form_class = PatientCreateForm
    inlines = [EchocardiographyInLine, GeneticResearchInLine, ImmunologicalResearchInLine, BodyMassIndexInLine,
               PilidogramInLine, BiochemicalBloodAnalysisInLine, CoronaryAngiographyInLine, ECGInLine]
    inlines_names = ["Echocardiography", "GeneticResearch", "ImmunologicalResearch", "BodyMassIndex",
                     "Pilidogram", "BiochemicalBloodAnalysis", "CoronaryAngiography", "ECG"]
    template_name = "medtools/heart_disease_tool.html"

    factory_kwargs = {'extra': 1, 'max_num': 1,
                      'can_order': False, 'can_delete': False}

    def get_context_data(self, **kwargs):
        context = super(HeartDiseaseToolPage, self).get_context_data(**kwargs)
        return dict(list(context.items()) + list(self.get_user_context().items()))

    def get_success_url(self):
        return self.object.get_absolute_url()


class HeartDiseaseToolUpdatePage(NamedFormsetsMixin, MenuMixin, UpdateWithInlinesView):
    model = Patient
    form_class = PatientCreateForm
    inlines = [EchocardiographyInLine, GeneticResearchInLine, ImmunologicalResearchInLine, BodyMassIndexInLine,
               PilidogramInLine, BiochemicalBloodAnalysisInLine, CoronaryAngiographyInLine, ECGInLine]
    inlines_names = ["Echocardiography", "GeneticResearch", "ImmunologicalResearch", "BodyMassIndex",
                     "Pilidogram", "BiochemicalBloodAnalysis", "CoronaryAngiography", "ECG"]
    template_name = "medtools/heart_disease_tool_update.html"

    factory_kwargs = {'extra': 3, 'max_num': 1,
                      'can_order': False, 'can_delete': False}

    def get_context_data(self, **kwargs):
        context = super(HeartDiseaseToolUpdatePage, self).get_context_data(**kwargs)
        context["surveys"] = Survey.objects.all()
        
        return dict(list(context.items()) + list(self.get_user_context().items()))

    def get_success_url(self):
        return self.object.get_absolute_url()


class SurveyPage(MenuMixin, DetailView, FormView):
    model = SurveyQuestion
    form_class = SurveyAnswerForm
    template_name = "medtools/survey.html"

    def get_success_url(self):
        survey_question_id =self.request.session["survey_question_id"]
        url = SurveyQuestion.objects.get(id=survey_question_id).get_next_question()
        if url is None:
            return reverse_lazy("heart-disease-tool-update", kwargs={"pk": self.request.session.get("patient_id")})

        return url

    def get_form_kwargs(self):
        kwargs = super(SurveyPage, self).get_form_kwargs()
        survey_question_id = list(filter(None, self.request.path.split("/")))[-1]
        self.request.session["survey_question_id"] = survey_question_id
        kwargs["survey_question"] = SurveyQuestion.objects.get(id=survey_question_id)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SurveyPage, self).get_context_data(**kwargs)
        return dict(list(context.items()) + list(self.get_user_context().items()))

    def form_valid(self, form):
        form.save()
        return super(SurveyPage, self).form_valid(form)

