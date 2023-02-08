from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.utils.translation import gettext_lazy as _
# forms.fields.Field.default_error_messages = {'required': _('No dots here'),}


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label=_("Логин"), widget=forms.TextInput(attrs={
        "class": "form-input",
        "type": "text",
        "name": "givenName",
        "id": "givenName",
        "maxlength": "255",
    }))
    password1 = forms.CharField(label=_("Пароль"), widget=forms.PasswordInput(attrs={
        "class": "form-input",
        "type": "password",
        "name": "password",
        "id": "password",
        "password": "true",
        "maxlength": "32",
    }))
    password2 = forms.CharField(label=_("Подтверждение пароля"), widget=forms.PasswordInput(attrs={
        "class": "form-input",
        "type": "password",
        "name": "password2",
        "id": "password2",
        "password": "true",
        "maxlength": "32",
    }))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={
        "class": "form-input",
        "type": "email",
        "name": "email",
        "id": "email",
        "maxlength": "90",
    }))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2",)

