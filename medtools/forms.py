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
            'patient': forms.Select(attrs={"class": "form-control", }),
            'mk': forms.Select(attrs={"class": "form-control", }),
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


class BodyMassIndexForm(forms.ModelForm):
    class Meta:
        model = BodyMassIndex
        exclude = ["patient"]

        widgets = {
            'mass': forms.TextInput(attrs={"class": "form-control", 'rows': 3}),
            'height': forms.TextInput(attrs={"class": "form-control", 'rows': 3}),
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
