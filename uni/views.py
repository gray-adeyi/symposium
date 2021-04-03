from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import (
    get_user_model,
    login,
    logout,)
from django.views import generic
from django.views import View
import logging
from . import forms

logger = logging.getLogger(__name__)
USER = get_user_model()


class GTemplate(generic.TemplateView):
    template_name = "uni/form_base.html"


class Register(View):
    """
    handles student sign up
    """
    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)
        self.template_name = 'uni/register.html'
        self.ctx = {'form': forms.RegisterForm()}

    def get(self, request):
        return render(request, self.template_name, self.ctx)

    def post(self, request):
        new_user = forms.RegisterForm(request.POST)
        if new_user.is_valid():
            user = USER.objects.create_user(
                    email=new_user.cleaned_data['email'],
                    username=new_user.cleaned_data['username'],
                    first_name=new_user.cleaned_data['first_name'],
                    last_name=new_user.cleaned_data['last_name'],
            )
            user.set_password(new_user.cleaned_data['password'])
            user.save()
            new_user.send_mail()
            messages.success(request, "Your accout was successfully set up, \
                            please activate your accout via the email we just\
                            sent to you.")
            return HttpResponseRedirect(reverse('uni:login'))
        else:
            self.ctx['form'] = new_user
            return self.get(request)


class Activate(View):
    """
    Activates a newly created account.
    """

    def get(self, request):
        pass


class Login(View):
    """
    serves the login page of the
    application
    """
    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        self.template_name = 'uni/login.html'
        self.ctx = {'form': forms.LoginForm()}

    def get(self, request):
        return render(request, self.template_name, self.ctx)

    def post(self, request):
        new_login = forms.LoginForm(request.POST)
        if new_login.is_valid():
            user = new_login.authenticate()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('uni:dashboard'))
            else:
                messages.error(request, "User not found!")
        else:
            messages.error(request, "Unable to login user")
            self.ctx['form'] = new_login
            return self.get(request)


def logout_view(request):
    """
    As the name suggests,
    it logs out users.
    """
    logout(request)
    messages.success(request, 'Logout successful')
    return HttpResponseRedirect(reverse('uni:login'))


class SendPasswordReset(generic.TemplateView):
    """
    View helps accept email to which the reset
    password page is sent.
    """
    template_name = 'uni/send_reset.html'


class PasswordReset(generic.TemplateView):
    """
    Responsible for updating user's password_validation
    """
    template_name = 'uni/reset.html'


class ActivateAccount(generic.TemplateView):
    """
    Responsible for activating users's accounts
    by ensuring that the email they supplied on
    registration acctually exists.
    """
    template_name = "uni/activate.html"


class Dashboard(generic.TemplateView):
    """
    Renders user dashboard based on the
    supplied data.
    """
    template_name = "uni/dashboard.html"
