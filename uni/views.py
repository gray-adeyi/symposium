from django.shortcuts import render
from django.views import generic
from django.views import View
# Create your views here.


class GTemplate(generic.TemplateView):
    template_name = "uni/form_base.html"


class Login(View):
    """
    serves the login page of the
    application
    """
    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        self.template_name = 'uni/login.html'
        self.ctx = {}

    def get(self, request):
        return render(request, self.template_name, self.ctx)


class Register(View):
    """
    handles student sign up
    """
    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)
        self.template_name = 'uni/register.html'
        self.ctx = {}

    def get(self, request):
        return render(request, self.template_name, self.ctx)


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
