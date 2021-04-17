from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class TestViews(TestCase):

    def test_register_page_works(self):
        response = self.client.get(reverse('uni:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uni/register.html')

    def test_register_new_user(self):
        pass

    def test_activate_account_page_works(self):
        pass

    def test_login_page_works(self):
        pass

    def test_user_login(self):
        pass

    def test_user_logout(self):
        pass

    def test_send_password_reset_works(self):
        response = self.client.get(reverse('uni:reset-link'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uni/send_reset.html')

    def test_password_reset(self):
        pass

    def test_student_dashboard_page_works(self):
        pass

    def test_student_profile_works(self):
        pass

    def test_leader_autorization_page_works(self):
        pass

    def test_leader_autorization_works(self):
        pass

    def test_create_symposium_works(self):
        pass

    def test_explore_symposium_page_works(self):
        pass

    def test_faq_page_works(self):
        pass

    def test_updated_user_info(self):
        pass

    def test_add_phone_number(self):
        pass

    def test_remove_phone_number(self):
        pass

    def test_join_symposium(self):
        pass
