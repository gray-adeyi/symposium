from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets
from django.contrib.auth import (
    get_user_model,
    authenticate,)
from django.core.mail import send_mail
from django.urls import reverse
from django import forms
import logging
from . import models

logger = logging.getLogger(__name__)
USER = get_user_model()


class RegisterForm(forms.Form):
    SPECIAL_CHARS = "~!@#$%^&*-_+=?"
    NUMS = '1234567890'

    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    confirm_password = forms.CharField(max_length=50)

    def clean(self):
        cleaned_data = super().clean()
        passwd = cleaned_data.get('password', None)
        cf_passwd = cleaned_data.get('confirm_password', None)
        if passwd != cf_passwd:
            self.add_error('password', forms.ValidationError(
                    "Passwords mismatch"))
        self.validate_password()
        self.validate_username()
        self.validate_email()

    def _validate_field(self, field, err_msg):
        """
        checks to see if a user with
        the field supplied already exists and raises
        an error is this conditions is met.
        """
        try:
            if field == 'username':
                try:
                    USER.objects.get(
                        username=self.cleaned_data[f'{field}'])
                    self.add_error(f'{field}', forms.ValidationError(err_msg))
                except USER.DoesNotExist:
                    pass
            elif field == 'email':
                try:
                    USER.objects.get(
                        email=self.cleaned_data[f'{field}'])
                    self.add_error(f'{field}', forms.ValidationError(err_msg))
                except USER.DoesNotExist:
                    pass
        except Exception as e:
            raise(e)

    def validate_password(self):
        """
        Method checks to see if the passwords meet
        the folllowing constraints.
        1. length >= 8
        2. contains a special character
        3. contains a number.
        """
        passwd = self.cleaned_data.get('password')
        contains_number = False
        contains_special_char = False
        if len(passwd) < 8:
            self.add_error('password', forms.ValidationError(
                    "Password length should be greater or equal to eight"
            ))

        for char in passwd:  # Test to see if number or special characters
            # are in the password
            if char in self.SPECIAL_CHARS:
                contains_special_char = True
            if char in self.NUMS:
                contains_number = True

        if not contains_number:
            self.add_error('password', forms.ValidationError(
                    "Password does not contain a number. \
                    please add at least one"
            ))

        if not contains_special_char:
            self.add_error('password', forms.ValidationError(
                    "Password does not contain a special character. \
                    please add at least one from `~!@#$%^&*-_+=?`"
            ))

    def validate_username(self):
        """
        checks to see if a user with
        the username already exists and raises
        an error is this conditions is met.
        """
        self._validate_field('username',
                             'User with this username already exists')

    def validate_email(self):
        """
        checks to see if a user with
        the email already exists and raises
        an error is this conditions is met.
        """
        self._validate_field('email',
                             'Email is already attached to an existing \
                             account.')

    def send_mail(self, request, usr_obj):
        link = self.create_student_data(usr_obj)
        link = "https://" + request.get_host() + reverse('uni:activate',
                                                         kwargs={'link': link})
        logger.info(f"Sending accout activation link to \
        {self.cleaned_data['email']}")

        message = f"""
        Dear {self.cleaned_data['first_name']},
        Your account has been successfully created, please
        follow this link to activate your account {link}

        Best Regards
        Gbenga@symposium
        [Notice: Ignore this email if you did not just attempt to create
        an account]
        """

        mail = MIMEMultipart()
        mail['From'] = 'admin@symposium.com'
        mail['To'] = self.cleaned_data['email']
        mail['Subject'] = "[Symposium] Activate account"
        msg = MIMEText(message, 'plain')
        mail.attach(msg)

        send_mail(
            "[Symposium] Activate account",
            mail.as_string(),
            "folarinolawale3415@gmail.com",
            [f"{self.cleaned_data['email']}"],
            fail_silently=False,
            )

    def create_student_data(self, usr_obj):
        """
        creates a `Student` model instance
        and relates it to the created user
        and returns the link needed for account
        activation.
        """
        student_data = models.Student.objects.create(
            basic_data=usr_obj,
        )
        return student_data.link


class LoginForm(forms.Form):
    FIELDS = {
        'one': 'email',  # TODO: Replace with enum.
        'two': 'username',
        'three': 'matric_no',
        'four': 'reg_no',
        }

    multi_field = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

    def clean(self):
        super().clean()
        self.validate_user_exists()

    def validate_user_exists(self):
        field = self.cleaned_data.get('multi_field')

        exists = False

        try:
            field_type = self.get_field_type()
            if field_type is not None:
                if field_type == 'username':
                    try:
                        USER.objects.get(username=field)
                        exists = True
                    except USER.DoesNotExist:
                        pass  # do nothing so that the `if not exists:` block
                        # executes.
                elif field_type == 'email':
                    try:
                        USER.objects.get(email=field)
                        exists = True
                    except USER.DoesNotExist:
                        pass  # do nothing so that the `if not exists:` block
                        # executes.
                elif field_type == 'matric_no':
                    try:
                        models.Student.objects.get(matric_no=field)
                        exists = True
                    except models.Student.DoesNotExist:
                        pass  # do nothing so that the `if not exists:` block
                        # executes.
                elif field_type == 'reg_no':
                    try:
                        models.Student.objects.get(reg_no=field)
                        exists = True
                    except models.Student.DoesNotExist:
                        pass  # do nothing so that the `if not exists:` block
                        # executes.
            else:
                pass  # TODO: handle inability to determine field type
        except Exception as e:
            raise(e)

        if not exists:
            self.add_error('multi_field', 'Cannot find a matching user')

    def _is_email(self, field):
        if(field.endswith('.com') and '@' in field):  # TODO: Replace
            # with RegEx
            logger.info("Field is an email")
            return True
        return False

    def _is_reg_no(self, field):
        ALPHABETS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if len(field) == 10:
            last_two_digits = field[-2:].upper()
            char_result = []
            for char in last_two_digits:
                if char in ALPHABETS:
                    char_result.append(True)
                else:
                    char_result.append(False)
            if char_result[0] and char_result[1]:
                try:
                    int(field[0:-2])
                    logger.info('Field is a Reg no')
                    return True
                except ValueError:
                    return False
                except Exception as e:
                    raise(e)
        return False

    def _is_matric_no(self, field):
        try:
            int(field)
            logger.info('Field is a Matric no')
            return True
        except ValueError:
            return False
        except Exception as e:
            raise(e)

    def _is_username(self, field):
        if(not self._is_email(field) and not self._is_reg_no(field)
           and not self._is_matric_no(field)):
            logger.info("Field is a username")
            return True
        return False

    def get_field_type(self):
        field = self.cleaned_data.get('multi_field')
        logger.info(f"Field is {field}")

        if self._is_email(field):
            return self.FIELDS['one']
        if self._is_username(field):
            return self.FIELDS['two']
        if self._is_matric_no(field):
            return self.FIELDS['three']
        if self._is_reg_no(field):
            return self.FIELDS['four']
        return None

    def authenticate(self):
        """
        Authenticates user and returns
        user instance.
        """
        field_type = self.get_field_type()
        if field_type is not None:
            if field_type == 'username':
                return authenticate(username=self.cleaned_data.get(
                    'multi_field'),
                    password=self.cleaned_data.get('password'))
            elif field_type == 'email':
                user = USER.objects.get(email=self.cleaned_data.get(
                    'multi_field'
                ))
                return authenticate(username=user.username,
                                    password=self.cleaned_data.get('password'))
            elif field_type == 'reg_no':
                user = models.Student.objects.get(
                    reg_no=self.cleaned_data['multi_field']).user
                return authenticate(username=user.username,
                                    password=self.cleaned_data.get('password'))
            elif field_type == 'matric_no':
                user = models.Student.objects.get(
                    matric_no=self.cleaned_data['multi_field']).user
                return authenticate(username=user.username,
                                    password=self.cleaned_data.get('password'))
            else:
                return None


class LeaderForm(forms.Form):
    OPTIONS = (
        ('n', 'Select Rank'),
        ('d', 'Deputy'),
        ('g', 'Governor'),
    )
    rank = forms.ChoiceField(choices=OPTIONS)


class SymposiumForm(forms.ModelForm):
    class Meta:
        model = models.Symposium
        fields = ['department',
                  'name',
                  'level',
                  'about',
                  'poster_image',
                  ]


class PhoneNumberForm(forms.Form):
    number = forms.CharField(max_length=14)


class UpdateUserForm(forms.Form):
    username = forms.CharField(max_length=50, required=False)
    email = forms.CharField(max_length=50, required=False)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    def clean(self):
        super().clean()
        self.validate('username', 'Username already exists')
        self.validate('username', 'Email is already attached to \
        another account')

    def validate(self, field, err_msg):
        if self.cleaned_data[field] is not None:
            if field == 'username':
                try:
                    user = USER.objects.get(username=self.cleaned_data[field])
                    if (user.email != self.cleaned_data['email'] and
                            user.first_name !=
                            self.cleaned_data['first_name']):
                        self.add_error(f'{field}',
                                       forms.ValidationError(err_msg))
                except USER.DoesNotExist:
                    pass
                except Exception as e:
                    raise(e)
            elif field == 'email':
                try:
                    user = USER.objects.get(email=self.cleaned_data[field])
                    if (user.username != self.cleaned_data['username'] and
                            user.first_name !=
                            self.cleaned_data['first_name']):
                        self.add_error(f'{field}',
                                       forms.ValidationError(err_msg))
                except USER.DoesNotExist:
                    pass
                except Exception as e:
                    raise(e)
            else:
                pass


class StudentForm(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = [
            'matric_no',
            'reg_no',
            'school_email',
            'address',
            'gender',
            'religion',
            'dob',
            'bio',
            'passport_photograph',
            'profile_picture',
            'signature',
            'state_of_origin',
        ]


class SendPasswordResetForm(forms.Form):

    email = forms.EmailField()

    def clean(self):
        super().clean()
        self.validate_email()

    def validate_email(self):
        """
        Ensures that the user with that email
        exists before sending a reset link to
        to the user.
        """
        email = self.cleaned_data.get('email')
        try:
            USER.objects.get(email=email)
        except USER.DoesNotExist:
            self.add_error('email', 'A user with the supplied email \
                does not exist.')
        except Exception as e:
            logger.error(str(e))

    def send_mail(self, request):
        # first update the old `Student.link` value with a new one.

        user = USER.objects.get(email=self.cleaned_data.get('email'))
        user.student_data.link = secrets.token_urlsafe(32)
        user.student_data.save()
        link = user.student_data.link
        link = "https://" + request.get_host() + reverse('uni:reset',
                                                         kwargs={'link': link})
        logger.info(f"Sending password reset link to \
        {self.cleaned_data['email']}")

        message = f"""
        Dear {user.first_name},
        Here's the link to reset your password. {link}

        Best Regards
        Gbenga@symposium
        [Notice: Ignore this email if you did not just attempt a
        password reset]
        """

        mail = MIMEMultipart()
        mail['From'] = 'admin@symposium.com'
        mail['To'] = self.cleaned_data['email']
        mail['Subject'] = "[Symposium] Password Reset"
        msg = MIMEText(message, 'plain')
        mail.attach(msg)

        send_mail(
            "[Symposium] Password Reset",
            mail.as_string(),
            "folarinolawale3415@gmail.com",
            [f"{self.cleaned_data['email']}"],
            fail_silently=False,
            )


class PasswordResetForm(forms.Form):
    SPECIAL_CHARS = "~!@#$%^&*-_+=?"
    NUMS = '1234567890'

    new_password = forms.CharField(max_length=50)
    confirm_password = forms.CharField(max_length=50)

    def clean(self):
        super().clean()
        self.validate_password()

    def validate_password(self):
        """
        Method checks to see if the passwords meet
        the folllowing constraints.
        1. length >= 8
        2. contains a special character
        3. contains a number.
        4. `new_password` matches `confirm_password`.
        """
        passwd = self.cleaned_data.get('new_password')
        cfrm_passwd = self.cleaned_data.get('confirm_password')
        if(cfrm_passwd != passwd):
            self.add_error('confirm_password', forms.ValidationError(
                "Password mismatch. please try again."))
        contains_number = False
        contains_special_char = False
        if len(passwd) < 8:
            self.add_error('new_password', forms.ValidationError(
                    "Password length should be greater or equal to eight"
            ))

        for char in passwd:  # Test to see if number or special characters
            # are in the password
            if char in self.SPECIAL_CHARS:
                contains_special_char = True
            if char in self.NUMS:
                contains_number = True

        if not contains_number:
            self.add_error('new_password', forms.ValidationError(
                    "Password does not contain a number. \
                    please add at least one"
            ))

        if not contains_special_char:
            self.add_error('new_password', forms.ValidationError(
                    "Password does not contain a special character. \
                    please add at least one from `~!@#$%^&*-_+=?`"
            ))

    def update_user_password(self, link):
        user = models.Student.objects.get(link=link).basic_data
        password = self.cleaned_data.get('confirm_password')
        if(password != '' or password is not None):
            user.set_password(password)
            user.save()
            logger.info(f"Updated the password of user: \
                {user.username}")
