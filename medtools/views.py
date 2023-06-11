from django.http import Http404
from django.views.generic import ListView, DetailView, FormView, CreateView
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

    def get_context_data(self, **kwargs):
        context = super(HeartDiseaseToolUpdatePage, self).get_context_data(**kwargs)
        surveys = Survey.objects.all().distinct()
        context["surveys"] = surveys
        print(self.object.get_overall_score())
        surveys_result = list()
        patient_id = self.request.session.get("patient_id")
        for survey in surveys:
            overall_score = survey.get_overall_score(patient_id)
            survey_results_set = survey.surveyresult_set.all()

            if survey_results_set.first() is None:
                context["INSD"] = survey.get_insd(patient_id)
                context["PRI"] = survey.get_pri(patient_id)
                continue

            if overall_score is None:
                continue

            for result in survey_results_set:
                if result.mark_from <= overall_score <= result.mark_to:
                    surveys_result.append(result.text)
                    break

        context["surveys_result"] = surveys_result

        return dict(list(context.items()) + list(self.get_user_context().items()))

    def get_success_url(self):
        return self.object.get_absolute_url()


class SurveyView(MenuMixin, FormView):
    template_name = "medtools/survey.html"

    def get_success_url(self):
        question_id = self.request.GET.get("question_id", None)
        url = SurveyQuestion.objects.get(id=question_id).get_next_question()
        if url is None:
            return reverse_lazy("heart-disease-tool-update", kwargs={"pk": self.request.session.get("patient_id")})

        return url

    def get_form_kwargs(self):
        kwargs = super(SurveyView, self).get_form_kwargs()
        question_id = self.request.GET.get("question_id", None)
        kwargs["survey_question"] = SurveyQuestion.objects.get(id=question_id)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SurveyView, self).get_context_data(**kwargs)
        question_id = self.request.GET.get("question_id", None)
        if question_id is None:
            raise Http404()

        context["question"] = SurveyQuestion.objects.get(id=question_id)
        context["me"] = 1
        return dict(list(context.items()) + list(self.get_user_context().items()))


class SurveyMultipleChoicePage(SurveyView):
    form_class = SurveyMultipleAnswerForm

    def form_valid(self, form):
        survey_answer = form.save(commit=False)
        survey_answer.patient = Patient.objects.get(id=self.request.session.get("patient_id"))
        survey_answer.save()
        form.save_m2m()
        return super(SurveyMultipleChoicePage, self).form_valid(form)


class SurveyPage(SurveyView):
    form_class = SurveyAnswerForm

    def form_valid(self, form, *args, **kwargs):
        survey_answer = form.save(commit=False)
        survey_answer.patient = Patient.objects.get(id=self.request.session.get("patient_id"))
        survey_answer.save()
        return super(SurveyPage, self).form_valid(form)


