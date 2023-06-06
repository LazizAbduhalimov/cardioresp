from django import forms
from django.forms import inlineformset_factory

from extra_views import InlineFormSetFactory

from medtools.models import *


class PatientCreateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = "__all__"

        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", 'rows': 3}),
            'sex': forms.Select(attrs={"class": "form-control", }),
            'age': forms.Select(attrs={"class": "form-control", }),
            'heart_rate': forms.TextInput(attrs={"class": "form-control", 'rows': 3}),
            'social_position': forms.Select(attrs={"class": "form-control", }),
            'pain_duration': forms.Select(attrs={"class": "form-control", }),
        }


class EchocardiographyForm(forms.ModelForm):
    class Meta:
        model = Echocardiography
        exclude = ["patient"]
        widgets = {
            'ejection_fraction': forms.NumberInput(attrs={"class": "form-control"}),
            'kcr': forms.NumberInput(attrs={"class": "form-control"}),
            'kdr': forms.NumberInput(attrs={"class": "form-control"}),
            'eslj': forms.NumberInput(attrs={"class": "form-control"}),
            'mjp': forms.NumberInput(attrs={"class": "form-control"}),
            'pj': forms.NumberInput(attrs={"class": "form-control"}),
            'mk': forms.Select(attrs={"class": "form-control", }),
            'lp': forms.NumberInput(attrs={"class": "form-control"}),
        }


class GeneticResearchForm(forms.ModelForm):
    class Meta:
        model = GeneticResearch
        exclude = ["patient"]

        widgets = {
            'IL_1b_511_TC': forms.Select(attrs={"class": "form-control", }),
            'IL_4_TC': forms.Select(attrs={"class": "form-control", }),
            'IL_10_819_CT': forms.Select(attrs={"class": "form-control", }),
            'TNF_a_GA': forms.Select(attrs={"class": "form-control", }),
        }


class ImmunologicalResearchForm(forms.ModelForm):
    class Meta:
        model = ImmunologicalResearch
        exclude = ["patient"]

        widgets = {
            'IL_1b': forms.NumberInput(attrs={"class": "form-control"}),
            'TNF_a': forms.NumberInput(attrs={"class": "form-control"}),
            'IL_4': forms.NumberInput(attrs={"class": "form-control"}),
            'IL_10': forms.NumberInput(attrs={"class": "form-control"}),
        }


class BodyMassIndexForm(forms.ModelForm):
    class Meta:
        model = BodyMassIndex
        exclude = ["patient"]

        widgets = {
            'mass': forms.NumberInput(attrs={"class": "form-control"}),
            'height': forms.NumberInput(attrs={"class": "form-control"}),
        }


class PilidogramForm(forms.ModelForm):
    class Meta:
        model = Pilidogram
        exclude = ["patient"]
        widgets = {
            'HS': forms.NumberInput(attrs={"class": "form-control"}),
            'HS_LLNP': forms.NumberInput(attrs={"class": "form-control"}),
            'HS_LLVP': forms.NumberInput(attrs={"class": "form-control"}),
            'TG': forms.NumberInput(attrs={"class": "form-control"}),
            'KAT': forms.NumberInput(attrs={"class": "form-control"}),
        }


class BiochemicalBloodAnalysisForm(forms.ModelForm):
    class Meta:
        model = BiochemicalBloodAnalysis
        exclude = ["patient"]
        widgets = {
            'ALAT': forms.NumberInput(attrs={"class": "form-control"}),
            'ACAT': forms.NumberInput(attrs={"class": "form-control"}),
            'HS_LLVP': forms.NumberInput(attrs={"class": "form-control"}),
            'creotenin': forms.NumberInput(attrs={"class": "form-control"}),
            'urea': forms.NumberInput(attrs={"class": "form-control"}),
            'uric_acid': forms.NumberInput(attrs={"class": "form-control"}),
            'bilirubin_common': forms.NumberInput(attrs={"class": "form-control"}),
            'bilirubin_direct': forms.NumberInput(attrs={"class": "form-control"}),
            'bilirubin_indirect': forms.NumberInput(attrs={"class": "form-control"}),
            'glucose': forms.NumberInput(attrs={"class": "form-control"}),
        }


class CoronaryAngiographyForm(forms.ModelForm):
    class Meta:
        model = CoronaryAngiography
        exclude = ["patient"]

        widgets = {
            'field': forms.Select(attrs={"class": "form-control", }),
        }


class ECGForm(forms.ModelForm):
    class Meta:
        model = ECG
        exclude = ["patient"]

        widgets = {
            'field': forms.Select(attrs={"class": "form-control", }),
        }


class SurveyAnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        survey_question = kwargs.pop('survey_question', None)
        super(SurveyAnswerForm, self).__init__(*args, **kwargs)
        self.fields['choice'].queryset = SurveyQuestionChoices.objects.filter(question=survey_question)

    class Meta:
        model = SurveyAnswer
        exclude = ["patient"]

        widgets = {
            'choice': forms.RadioSelect(attrs={"class": "form-check-input", }),
        }


class EchocardiographyInLine(InlineFormSetFactory):
    form_class = EchocardiographyForm
    model = Echocardiography


class GeneticResearchInLine(InlineFormSetFactory):
    form_class = GeneticResearchForm
    model = GeneticResearch


class ImmunologicalResearchInLine(InlineFormSetFactory):
    form_class = ImmunologicalResearchForm
    model = ImmunologicalResearch


class BodyMassIndexInLine(InlineFormSetFactory):
    form_class = BodyMassIndexForm
    model = BodyMassIndex


class PilidogramInLine(InlineFormSetFactory):
    form_class = PilidogramForm
    model = Pilidogram


class BiochemicalBloodAnalysisInLine(InlineFormSetFactory):
    form_class = BiochemicalBloodAnalysisForm
    model = BiochemicalBloodAnalysis


class CoronaryAngiographyInLine(InlineFormSetFactory):
    form_class = CoronaryAngiographyForm
    model = CoronaryAngiography


class ECGInLine(InlineFormSetFactory):
    form_class = ECGForm
    model = ECG
