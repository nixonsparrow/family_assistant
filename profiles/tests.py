import time

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.core import mail


class ProfilePageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='TestPassword123!@#')
        self.response = self.client.get(reverse_lazy('profile'))

    def test_login(self):
        self.client.login(username='TestUser', password='TestPassword123!@#')
        response = self.client.get(reverse_lazy('profile'))
        self.assertEqual(response.status_code, 200)

    def test_uses_proper_template_only_logged_in(self):
        self.assertTemplateNotUsed(self.response, 'profiles/profile.html')

        self.client.login(username='TestUser', password='TestPassword123!@#')
        response_after_login = self.client.get(reverse_lazy('profile'))
        self.assertTemplateUsed(response_after_login, 'profiles/profile.html')


class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='TestPassword123!@#', email='testuser@gmail.com')

    def test_password_reset(self):

        # First we get the initial password reset form.
        # This is not strictly necessary, but I included it for completeness
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'profiles/password_reset.html')

        # post the response with our "email address"
        response = self.client.post(reverse('password_reset'), {'email': 'testuser@gmail.com'})
        self.assertEqual(response.status_code, 302)
        # check email response
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password reset on testserver')

        # get the token and userid from the response
        token = response.context[0]['token']
        uid = response.context[0]['uid']

        # Now we can use the token to get the password change form
        response = self.client.get(reverse('password_reset_confirm', kwargs={'token': token, 'uidb64': uid}))
        self.assertRedirects(response, reverse('password_reset_confirm', kwargs={'token': 'set-password', 'uidb64': uid}),
                             status_code=302, target_status_code=200, fetch_redirect_response=True)

        # Now we post to the same url with our new password:
        # response = self.client.post(reverse('password_reset_confirm', kwargs={'token': token, 'uidb64': uid}),
        #                        {'new_password1': 'TestPassword123!@#', 'new_password2': 'TestPassword123!@#'})
        # self.assertRedirects(response, reverse('password_reset_complete'),
        #                      status_code=302, target_status_code=200, fetch_redirect_response=True)
