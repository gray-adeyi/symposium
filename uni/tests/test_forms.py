from django.test import TestCase
from django.core import mail
from uni import forms
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)


class TestForms(TestCase):

    def test_register_form(self):
        form = forms.RegisterForm({
            'email': 'coyotedevmail@gmail.com',
            'username': 'coyote',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': '1cleanCode!',
            'confirm_password': '1cleanCode!',
        })
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
        pass

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
