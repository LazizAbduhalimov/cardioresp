from django import forms
from blogs.models import Article, Comment
from modeltranslation.forms import TranslationModelForm
from django.utils.translation import gettext_lazy as _


class ArticleCreateForm(TranslationModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "annotation",
            "for_quoting",
            "doi",
            "file",
            # "authors_text",
            "tags",
            "is_draft",
        ]
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'for_quoting': forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            'doi': forms.TextInput(attrs={"class": "form-control", }),
            'file': forms.FileInput(attrs={"class": "form-control", }),
            'linked_volume': forms.Select(attrs={"class": "form-control", }),
            'chapter': forms.Select(attrs={"class": "form-control", }),
            'authors': forms.SelectMultiple(attrs={"class": "form-control", }),
            # 'authors_text': forms.TextInput(attrs={"class": "form-control", }),
            'tags': forms.SelectMultiple(attrs={"class": "form-control", }),
        }


class CommentCreateForm(TranslationModelForm):
    class Meta:
        model = Comment
        fields = [
            "text",
            "is_recommended",
        ]
        widgets = {
            'text': forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
        }
        labels = {
            "text": _("Ваш комментарий"),
            "is_recommended": _("Рекомендовать статью для публикации?")
        }