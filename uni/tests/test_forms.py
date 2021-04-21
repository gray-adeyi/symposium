from django.test import TestCase
from django.core import mail
from uni import forms
from uni import models
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)


USER_DATA_1 = {
    'email': 'coyotedevmail@gmail.com',
    'username': 'coyote',
    'first_name': 'John',
    'last_name': 'Doe',
    'password': '1cleanCode!',
    'confirm_password': '1cleanCode!',
}

USER_DATA_2 = {
    'email': 'coyotedevmail01@gmail.com',
    'username': 'coyote99',
    'first_name': 'John',
    'last_name': 'Doe',
    'password': '1cleanCode!',
    'confirm_password': '1cleanCode!',
}
STUDENT_DATA_1 = {
    'reg_no': '12445660aj',
    'matric_no': '1905004590'
}

class TestForms(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email=USER_DATA_1[
                                                'email'],
                                            username=USER_DATA_1['username'],
                                            first_name=USER_DATA_1[
                                                'first_name'],
                                            last_name=USER_DATA_1['last_name'])
        self.user.set_password(USER_DATA_1['password'])
        self.user.save()
        self.student = models.Student.objects.create(basic_data=self.user,
                                                     reg_no=STUDENT_DATA_1[
                                                        'reg_no'],
                                                     matric_no=STUDENT_DATA_1[
                                                        'matric_no'])

    def test_register_form(self):
        form = forms.RegisterForm(USER_DATA_2)
        self.assertTrue(form.is_valid())
        user = get_user_model().objects.create_user(email=form.cleaned_data[
                                                'email'],
                                            username=form.cleaned_data[
                                                'username'],
                                            first_name=form.cleaned_data[
                                                'first_name'],
                                            last_name=form.cleaned_data[
                                                'last_name'])
        user.set_password(form.cleaned_data['password'])
        user.save()

        with self.assertLogs('uni.forms', level='INFO') as cm:
            form.send_mail(user)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         '[Symposium] Activate account')
        self.assertGreaterEqual(len(cm.output), 1)

    def test_login_form(self):
        form_login_with_email = forms.LoginForm({
            'multi_field': USER_DATA_1['email'],
            'password': USER_DATA_1['password']
        })
        form_login_with_username = forms.LoginForm({
            'multi_field': USER_DATA_1['username'],
            'password': USER_DATA_1['password']
        })
        form_login_with_matric_no = forms.LoginForm({
            'multi_field': STUDENT_DATA_1['matric_no'],
            'password': USER_DATA_1['password']
        })
        form_login_with_reg_no = forms.LoginForm({
            'multi_field': STUDENT_DATA_1['reg_no'],
            'password': USER_DATA_1['password']
        })
        self.assertTrue(form_login_with_email.is_valid())
        self.assertTrue(form_login_with_username.is_valid())
        self.assertTrue(form_login_with_matric_no.is_valid())
        self.assertTrue(form_login_with_reg_no.is_valid())

    def test_leader_form(self):
        pass

    def test_symposium_form(self):
        pass

    def test_phone_number_form(self):
        pass

    def test_updat_user_form(self):
        pass

    def test_student_form(self):
        pass
