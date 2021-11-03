from todo.models import Task
from django.test import TestCase
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver


class ToDoTests(TestCase):

    def test_uses_main_template(self):
        response = self.client.get('/todo/')

        # can we see proper template?
        self.assertTemplateUsed(response, 'todo/main.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/todo/', data={'new_task': 'Test Task'})

        # have we added a new object to the database?
        self.assertEqual(Task.objects.count(), 1, msg='Task was NOT added to the database.')
        new_item = Task.objects.first()
        self.assertEqual(new_item.title, 'Test Task', msg='Wrong task was added to the database.')
