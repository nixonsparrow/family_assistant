from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse_lazy


class ProfilePageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
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
