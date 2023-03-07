from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils.translation import get_language

from blogs.models import Volume
from registration.forms import RegisterUserForm
from main_app.models import Page
from main_app.utils import MenuMixin
from .utils import account_activation_token


User = get_user_model()


class Registration(MenuMixin, ListView):
    model = User
    template_name = "registration/registration.html"

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        links = Page.objects.filter(linklocation__title="About us")
        menu_links = Page.objects.filter(linklocation__title="Menu")
        side_bar_links = Page.objects.filter(linklocation__title="Side bar")
        try:
            next_volume = Volume.objects.filter(status_str="Следующий")[0]
        except:
            next_volume = None
        current_path = str(self.request.path)[3:]

        return render(request, 'registration/registration.html', {'form': form,
                                                                  'links': links,
                                                                  'menu_links': menu_links,
                                                                  'side_bar_links': side_bar_links,
                                                                  'next_volume': next_volume,
                                                                  'current_path': current_path})

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponseRedirect(reverse_lazy("registration-confirm"))
        else:
            return render(request, self.template_name, {"form": form})


def activate(request, uidb64, token):
    # User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse_lazy("successful-registration"))
    else:
        return HttpResponseRedirect(reverse_lazy("invalid-link"))


class EmailConfirmation(MenuMixin, ListView):
    model = User
    template_name = "registration/email_confirm_page.html"

    def get_context_data(self, **kwargs):
        context = super(EmailConfirmation, self).get_context_data(**kwargs)

        return dict(list(context.items()) + list(self.get_user_context().items()))


class SuccessfulRegistration(MenuMixin, ListView):
    model = User
    template_name = "registration/email_activation_page.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessfulRegistration, self).get_context_data(**kwargs)

        return dict(list(context.items()) + list(self.get_user_context().items()))


class InvalidLink(MenuMixin, ListView):
    model = User
    template_name = "registration/invalid_link.html"

    def get_context_data(self, **kwargs):
        context = super(InvalidLink, self).get_context_data(**kwargs)

        return dict(list(context.items()) + list(self.get_user_context().items()))


class LoginUser(MenuMixin, LoginView):
    form_class = AuthenticationForm
    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):
        print(self.request.META.get('HTTP_REFERER'))
        context = super(LoginUser, self).get_context_data(**kwargs)

        return dict(list(context.items()) + list(self.get_user_context().items()))

    def get_success_url(self):
        print(get_language())
        return f"/{get_language()}/home/"
