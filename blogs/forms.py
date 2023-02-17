from django import forms
from .models import Article
from modeltranslation.forms import TranslationModelForm


class ArticleCreateForm(TranslationModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "annotation",
            "for_quoting",
            "doi",
            "file",
            "authors_text",
            "tags",
        ]
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control", }),
            'for_quoting': forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            'doi': forms.TextInput(attrs={"class": "form-control", }),
            'file': forms.FileInput(attrs={"class": "form-control", }),
            'linked_volume': forms.Select(attrs={"class": "form-control", }),
            'chapter': forms.Select(attrs={"class": "form-control", }),
            'authors': forms.SelectMultiple(attrs={"class": "form-control", }),
            'authors_text': forms.TextInput(attrs={"class": "form-control", }),
            'tags': forms.SelectMultiple(attrs={"class": "form-control", }),
        }
