import datetime
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
    template_name = "uni/tables.html"


class Register(View):
    """
    handles student sign up
    """

    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)
        self.template_name = 'uni/register.html'
        self.ctx = {
            'form': forms.RegisterForm(),
            'site_info': SiteInfo.objects.filter().first()}

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
            new_user.send_mail(request, user)
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
        return HttpResponseRedirect(reverse('uni:login'))


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
            'site_info': SiteInfo.objects.filter().first()}

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
                messages.error(request, "Invalid Email/Username/Matric no/\
                    Reg no & password combination!")
                return HttpResponseRedirect(reverse('uni:login'))
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


class SendPasswordReset(View):
    """
    View helps accept email to which the reset
    password page is sent.
    """

    def __init__(self, *args, **kwargs):
        self.template_name = 'uni/send_reset.html'
        self.ctx = {
            'form': forms.SendPasswordResetForm()
        }

    def get(self, request):
        return render(request, self.template_name, self.ctx)

    def post(self, request):
        send_password_reset = forms.SendPasswordResetForm(request.POST)
        if send_password_reset.is_valid():
            send_password_reset.send_mail(request)
            messages.success(request, f"A password reset link has been sent \
                to {send_password_reset.cleaned_data.get('email')}")
            return HttpResponseRedirect(reverse('uni:reset-link'))
        else:
            messages.error(request, f"{send_password_reset.errors}")
            self.ctx['form'] = send_password_reset
            return self.get(request)


class PasswordReset(View):
    """
    Responsible for updating user's password_validation
    """

    def __init__(self, *args, **kwargs):
        self.template_name = 'uni/reset.html'
        self.ctx = {
            'form': forms.PasswordResetForm(),
        }

    def get(self, request, *args, **kwargs):
        self.ctx['link'] = kwargs['link']
        try:
            models.Student.objects.get(link=kwargs['link'])
            return render(request, self.template_name, self.ctx)
        except models.Student.DoesNotExist:
            messages.error("You tried accessing an invalid link")
            return HttpResponseRedirect(reverse('uni:login'))
        except Exception as e:
            logger.error(str(e))
            return HttpResponseRedirect(reverse('uni:login'))

    def post(self, request, *args, **kwargs):
        password_reset = forms.PasswordResetForm(request.POST)
        if(password_reset.is_valid()):
            password_reset.update_user_password(kwargs['link'])
            messages.success(request, "Password successfully updated!")
            return HttpResponseRedirect(reverse('uni:login'))
        else:
            messages.error(request, "An error occured")
            logger.info("i was hit")
            self.ctx['form'] = password_reset
            return self.get(request, link=kwargs['link'])


class Dashboard(generic.View):
    """
    Renders user dashboard based on the
    supplied data.
    """

    def __init__(self, *args, **kwargs):
        self.template_name = "uni/dashboard.html"
        self.ctx = {
            'site_info': SiteInfo.objects.filter().first(),
            'date': datetime.date.today()
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
            'site_info': SiteInfo.objects.filter().first()
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
                logger.info("member_of: \
                {student_data.cleaned_data.get('member_of')}")
                logger.info("basic_data: \
                {student_data.cleaned_data.get('basic_data')}")
                logger.info("matric_no: \
                {student_data.cleaned_data.get('matric_no')}")
                logger.info("reg_no: \
                {student_data.cleaned_data.get('reg_no')}")
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
                         f"class group {form.cleaned_data['name']} \
                         successfully created.")
        return HttpResponseRedirect(reverse('uni:dashboard'))


class ExploreSymposium(generic.ListView):
    """
    This view serves all the class groups
    also known as symposiums and used interchangably
    """
    template_name = 'uni/expore-symposiums.html'
    context_object_name = 'class_groups'
    paginate_by = 24
    model = models.Symposium


class FAQView(generic.ListView):
    """
    This view serves all FAQs particular to
    the request.user class group.
    """
    template_name = 'uni/faq.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        return models.FAQ.objects.filter(symposium=self.request.
                                         user.student_data.member_of)


class AssignmentView(generic.DetailView):
    template_name = "uni/assignment.html"
    context_object_name = 'assignment'

    def get_queryset(self):
        return models.Assignment.objects.filter(
            symposium=self.request.user.student_data.member_of,
            pk=self.kwargs['pk'])

###################################################
#
#   FUNCTION BASED VIEWS
#
###################################################


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


def join_symposium(request, pk):
    if not request.user.is_anonymous:
        symposium = models.Symposium.objects.get(pk=pk)
        request.user.student_data.member_of = symposium
        request.user.student_data.save()
        messages.success(request, f"You have been added to {symposium.name}")
        logger.info(f"{request.user} added to {symposium}")
        return HttpResponseRedirect(reverse('uni:dashboard'))
    else:
        messages.error(request, f"Can't join a class group until you're \
        logged in")
        return HttpResponseRedirect(reverse('uni:expore-classes'))
