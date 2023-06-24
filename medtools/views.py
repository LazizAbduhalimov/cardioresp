from io import BytesIO

from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, DeleteView
from docx import Document
from extra_views import UpdateWithInlinesView, CreateWithInlinesView, NamedFormsetsMixin
from django.utils.translation import gettext_lazy as _

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

    def form_valid(self, form):
        form.save()
        self.request.session["patient_id"] = self.object.pk
        return super(HeartDiseaseToolPage, self).form_valid(form)


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
        surveys_ratio_choice = surveys.filter(surveyquestion__has_multiple_choice=False)
        context["surveys_ratio_choice"] = surveys_ratio_choice
        surveys_multiple_choice = surveys.filter(surveyquestion__has_multiple_choice=True)
        context["surveys_multiple_choice"] = surveys_multiple_choice
        surveys_result = list()
        patient_id = self.request.session.get("patient_id")
        for survey in surveys_ratio_choice:
            overall_score = survey.get_overall_score(patient_id)
            survey_results_set = survey.surveyresult_set.all()

            if overall_score is None:
                continue

            for result in survey_results_set:
                if result.mark_from <= overall_score <= result.mark_to:
                    surveys_result.append(result.text)
                    break

        for survey in surveys_multiple_choice:
            pri = survey.get_pri(patient_id)
            insd = survey.get_insd(patient_id)
            if (pri or insd) is not None:
                context["INSD"] = insd
                context["PRI"] = pri

        context["surveys_result"] = surveys_result

        return dict(list(context.items()) + list(self.get_user_context().items()))

    def get_success_url(self):
        return self.object.get_absolute_url()


class HeartDiseaseToolDeletePage(DeleteView):
    model = Patient
    template_name = "medtools/heart_disease_tool_delete.html"
    success_url = reverse_lazy("heart-disease-tool")


class SurveyView(MenuMixin, FormView):
    template_name = "medtools/survey.html"

    def get_success_url(self):
        question_id = self.request.GET.get("question_id", None)
        url = SurveyQuestion.objects.get(id=question_id).get_next_question()
        if url is None:
            messages.add_message(
                self.request, messages.SUCCESS,
                "Опросник пройден"
            )
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
        context["GET_params"] = f"?question_id={question_id}"
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


def GetDocxFile(request, pk):
    """Return .docx file of the result of the HeartDiseaseToolUpdatePage"""
    patient = get_object_or_404(Patient, pk=pk)
    document = Document()
    docx_title = "result.docx"

    text = str()
    text += "{}, {} \n".format(patient.get_pain_duration_text(), patient.ecg.get_field_display())
    document.add_paragraph(text)

    text = _("Осложнения") + "\n"
    for disease in patient.get_disease_list():
        text += "{} \n".format(disease)

    risk_group = patient.get_risk_group()
    if risk_group is not None:
        text += "{} \n".format(risk_group)

    try:
        mass_index = patient.bodymassindex.get_mass_disease()
        text += "{} \n".format(mass_index)
    except ObjectDoesNotExist:
        pass

    try:
        for disease in patient.immunologicalresearch.get_disease_list():
            document.add_paragraph(disease)
    except ObjectDoesNotExist:
        pass

    try:
        for disease in patient.biochemicalbloodanalysis.get_disease_list():
            text += "{} \n".format(disease)
    except ObjectDoesNotExist:
        pass

    try:
        for disease in patient.lipidogram.get_disease_list():
            text += "{} \n".format(disease)
    except ObjectDoesNotExist:
        pass

    document.add_paragraph(text)

    text = _("Показатели ЭХОКГ") + "\n"
    for disease in patient.echocardiography.get_disease_list():
        text += "{} \n".format(disease)
    document.add_paragraph(text)

    text = ""
    surveys = Survey.objects.all().distinct()
    for survey in surveys:
        overall_score = survey.get_overall_score(pk)
        survey_results_set = survey.surveyresult_set.all()

        if survey_results_set.first() is None and (survey.get_insd(pk) and survey.get_pri(pk)):
            insd = _("Индекс числа выбранных дескрипторов")
            pri = _("Ранговой индекс боли")
            text += "{}: {}\n".format(insd, survey.get_insd(pk))
            text += "{}: {}\n".format(pri, survey.get_pri(pk))
            continue

        if overall_score is None:
            continue

        for result in survey_results_set:
            if result.mark_from <= overall_score <= result.mark_to:
                text += result.text + "\n"
                break

    if text != "":
        text = _("Результаты опросников") + "\n" + text

    document.add_paragraph(text)
    document.add_page_break()

    # Prepare document for download
    # -----------------------------
    f = BytesIO()
    document.save(f)
    length = f.tell()
    f.seek(0)
    response = HttpResponse(
        f.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=' + docx_title
    response['Content-Length'] = length
    return response
