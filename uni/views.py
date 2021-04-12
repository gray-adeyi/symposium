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
from main.models import SiteInfo
from . import (
    forms,
    models,
    )

logger = logging.getLogger(__name__)
USER = get_user_model()


class GTemplate(generic.TemplateView):
    template_name = "uni/landing-page.html"


class Register(View):
    """
    handles student sign up
    """
    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)
        self.template_name = 'uni/register.html'
        self.ctx = {
            'form': forms.RegisterForm(),
            'site_info': SiteInfo.objects.get()}

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
            new_user.send_mail(user)
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

    def get(self, request, link):
        student_data = models.Student.objects.get(link=link)
        student_data.is_activated = True
        student_data.save()
        messages.success(request, "Your account has been activated.")
        return HttpResponseRedirect(reverse('uni:dashboard'))


class Login(View):
    """
    serves the login page of the
    application
    """
    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        self.template_name = 'uni/login.html'
        self.ctx = {
            'form': forms.LoginForm(),
            'site_info': SiteInfo.objects.get()}

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


class Dashboard(generic.View):
    """
    Renders user dashboard based on the
    supplied data.
    """
    def __init__(self, *args, **kwargs):
        self.template_name = "uni/dashboard.html"
        self.ctx = {
            'site_info': SiteInfo.objects.get()
        }

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name, self.ctx)
        else:
            messages.error(request, "Your are required to login before \
                accessing this page.")
            return HttpResponseRedirect(reverse('uni:login'))


class Profile(generic.View):
    """
    Holds logic for the user
    profile page.
    """
    def __init__(self, user_form=None, number_form=None, *args, **kwargs):
        self.template_name = "uni/profile.html"
        self.ctx = {
            'site_info': SiteInfo.objects.get()
        }
        if user_form is not None:
            self.ctx['user_form'] = user_form
        if number_form is not None:
            self.ctx['number_form'] = number_form

    def get(self, request):
        if request.user.is_authenticated:
            user_info = forms.StudentForm(instance=request.user.student_data)
            self.ctx['student_data_form'] = user_info
            return render(request, self.template_name, self.ctx)
        else:
            messages.error(request, "You're required to login to \
                access this page.")
            return HttpResponseRedirect(reverse('uni:login'))

    def post(self, request):
        if request.user.is_authenticated:
            student_data = forms.StudentForm(request.POST, request.FILES,
                                             instance=request.user.
                                             student_data)
            if student_data.is_valid():
                logger.info("member_of: {student_data.cleaned_data.get('member_of')}")
                logger.info("basic_data: {student_data.cleaned_data.get('basic_data')}")
                logger.info("matric_no: {student_data.cleaned_data.get('matric_no')}")
                logger.info("reg_no: {student_data.cleaned_data.get('reg_no')}")
                student_data.save()
                messages.success(request, "Update successful")
                return HttpResponseRedirect(reverse('uni:profile'))
            else:
                logger.error(f"{student_data.errors}")
                self.ctx['student_data_form'] = student_data
                return self.get(request)
        else:
            return HttpResponseRedirect(reverse('uni:login'))


class LeaderAuthorization(generic.View):
    """
    This view authorizes Class Governors
    and Deputites.

    Note: Requires a better logic as it
    does not restrain a regular user from
    getting authorized as a class leader.
    perhaps this view will be deprecated
    in the future and class leaders will
    have to contact the site admin directly.
    """
    def __init__(self, *args, **kwargs):
        self.template_name = "uni/authorize.html"
        self.ctx = {'form': forms.LeaderForm()}

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name, self.ctx)
        else:
            messages.error(request, "You're required to login to \
                access this page.")
            return HttpResponseRedirect(reverse('uni:login'))

    def post(self, request):
        if request.user.is_authenticated:
            form = forms.LeaderForm(request.POST)
            if form.is_valid():
                rank = form.cleaned_data.get('rank', None)
                if rank is not None:
                    if rank == 'g':
                        request.user.student_data.is_governor = True
                        request.user.student_data.save()
                        messages.success(request, "You have been authorized \
                                         as a class governor.")
                    elif rank == 'd':
                        request.user.student_data.is_deputy = True
                        request.user.student_data.save()
                        messages.success(request, "You have been authorized \
                        as a class deputy governor.")
                    elif rank == 'n':
                        pass
                    return HttpResponseRedirect(reverse('uni:create-class'))
        else:
            messages.error(request, "You're required to login to \
                access this page.")
            return HttpResponseRedirect(reverse('uni:login'))


class CreateSymposium(generic.CreateView):
    model = models.Symposium
    form_class = forms.SymposiumForm
    template_name = 'uni/class-factory.html'

    def form_valid(self, form):
        symposium = form.save(self.request)
        logger.info(f"symposium is {symposium}")
        user = self.request.user  # Adds the user to the symposium
        # after creation
        user.student_data.member_of = symposium
        user.student_data.save()
        logger.info(f"{user} is now a member of {user.student_data.member_of}")
        messages.success(self.request,
                         f"class {form.cleaned_data['name']} \
                         successfully created")
        return HttpResponseRedirect(reverse('uni:dashboard'))


def updated_user_info(request):
    if request.user.is_authenticated and request.method == 'POST':
        new_user_data = forms.UpdateUserForm(request.POST)
        if new_user_data.is_valid():
            user = request.user
            logger.info(f'new firstname is \
                        {new_user_data.cleaned_data.get("first_name")}')
            user.first_name = new_user_data.cleaned_data.get('first_name',
                                                             user.first_name)
            user.last_name = new_user_data.cleaned_data.get('last_name',
                                                            user.last_name)
            user.username = new_user_data.cleaned_data.get('username',
                                                           user.username)
            user.email = new_user_data.cleaned_data.get('email',
                                                        user.email)
            user.save()
            messages.success(request, "Update was successful")
            return HttpResponseRedirect(reverse('uni:profile'))
        else:
            logger.error(f"An error occured {new_user_data.errors}")
            return Profile(user_form=new_user_data).get(request)
    else:
        return HttpResponseRedirect(reverse('uni:login'))


def add_phone_number(request):
    if request.user.is_authenticated and request.method == 'POST':
        new_number = forms.PhoneNumberForm(request.POST)
        if new_number.is_valid():
            number = models.StudentPhoneNumber(
                                               student=request.user.
                                               student_data,
                                               number=new_number.
                                               cleaned_data.get('number'))
            number.save()
            return HttpResponseRedirect(reverse('uni:profile'))
        else:
            logger.error(f"{new_number.errors}")
            messages.error(request, "An error occured while trying to \
            add phone number")
            return Profile(number_form=new_number).get(request)
    else:
        return HttpResponseRedirect(reverse('uni:login'))


def remove_phone_number(request, id):
    if request.user.is_authenticated and request.method == 'GET':
        try:
            number = models.StudentPhoneNumber.objects.get(student=request.
                                                           user.student_data,
                                                           pk=id)
            number.delete()
            messages.success(request, "Phone number successfully removed")
            return HttpResponseRedirect(reverse('uni:profile'))
        except models.StudentPhoneNumber.DoesNotExist:
            messages.error(request, "Phone number does not exist")
            return HttpResponseRedirect(reverse('uni:profile'))
        except Exception as e:
            logger.error(str(e))
            return HttpResponseRedirect(reverse('uni:profile'))

    else:
        return HttpResponseRedirect(reverse('uni:login'))
