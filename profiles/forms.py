from django import forms
from django.core.exceptions import ValidationError

from blogs.models import Article, Comment
from modeltranslation.forms import TranslationModelForm
from django.utils.translation import gettext_lazy as _


class ArticleCreateForm(TranslationModelForm):
    error_css_class = "alert alert-danger"

    class Meta:
        model = Article
        fields = [
            "title",
            "annotation",
            "for_quoting",
            "doi",
            "file",
            "authors",
            "tags_text",
            "is_draft",
        ]
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'for_quoting': forms.Textarea(attrs={"class": "form-control", 'rows': 3}),
            'doi': forms.TextInput(attrs={"class": "form-control", }),
            'file': forms.FileInput(attrs={"class": "form-control", }),
            'linked_volume': forms.Select(attrs={"class": "form-control", }),
            'chapter': forms.Select(attrs={"class": "form-control", }),
            'authors': forms.SelectMultiple(attrs={"class": "select-1 form-control", "multiple": "multiple"}),
            # 'authors_text': forms.TextInput(attrs={"class": "form-control", }),
            'tags_text': forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            'authors': "Соавторы",
            'tags_text': "Ключевые слова"
        }

    def clean_tags_text(self):
        tags_text = self.cleaned_data['tags_text']
        tags = str(tags_text).replace(" ", "").replace(";", ",").split(",")
        if len(tags) < 5:
            raise ValidationError(_("В статье должно быть более 5 ключевых слов"))
        return tags_text

    def clean_annotation(self):
        annotation = self.cleaned_data['annotation']
        if len(annotation.split()) < 100:
            raise ValidationError(_("Аннотация статьи должна содержать более 100 слов"))
        return annotation


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