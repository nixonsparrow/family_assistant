from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from .models import Task
from .forms import NewTaskForm


class HomePageTestCase(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse_lazy('homepage'))

    def test_site_header(self):
        self.assertContains(self.response, 'Family Helper')

    def test_template(self):
        self.assertTemplateUsed(self.response, 'homepage.html')


class LogInTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='12345')

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'TestUser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,  reverse('homepage'))

    def test_login2(self):
        self.assertTrue(self.client.login(username='TestUser', password='12345'))


class ToDoTaskListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='12345')
        self.client.login(username='TestUser', password='12345')

        self.task_1 = Task.objects.create(title='First Task')
        self.task_2 = Task.objects.create(title='Second Task')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('todo-all-tasks'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,  f"/login/?next={reverse_lazy('todo-all-tasks')}")

    def test_template(self):
        response = self.client.get(reverse_lazy('todo-all-tasks'))

        # can we see proper template?
        self.assertTemplateUsed(response, 'todo/task_list.html')

    def test_if_shows_tasks(self):
        response = self.client.get(reverse_lazy('todo-all-tasks'))
        self.assertContains(response, self.task_1.title)
        self.assertContains(response, self.task_2.title)


class ToDoNewTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='12345')
        self.client.login(username='TestUser', password='12345')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('todo-new-task'))
        self.assertRedirects(response, f"/login/?next={reverse_lazy('todo-new-task')}")

    def test_response_if_logged_in(self):
        response = self.client.get(reverse('todo-new-task'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'TestUser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(reverse('todo-new-task'))
        self.assertTemplateUsed(response, 'todo/task_form.html')

    def test_new_task_can_save_a_POST_request(self):
        self.client.post(reverse('todo-new-task'), data={'title': 'Test Task'})

        # have we added a new object to the database?
        self.assertEqual(Task.objects.count(), 1, msg='Task was NOT added to the database.')
        new_item = Task.objects.first()
        self.assertEqual(new_item.title, 'Test Task', msg='Wrong task was added to the database.')
        self.assertFalse(new_item.is_finished, msg='Task was created as completed.')

    def test_redirects_after_POST(self):
        response = self.client.post(reverse_lazy('todo-new-task'), data={'title': 'Test Task'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse_lazy('todo-all-tasks'))

    def test_has_form(self):
        response = self.client.get(reverse_lazy('todo-new-task'))
        form = response.context['form']
        self.assertIsInstance(form, NewTaskForm)

    def test_html(self):
        response = self.client.get(reverse_lazy('todo-new-task'))
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="text"', 1)
        self.assertContains(response, 'type="submit"', 1)

    def test_csrf(self):
        response = self.client.get(reverse_lazy('todo-new-task'))
        self.assertContains(response, 'csrfmiddlewaretoken')


class TasksMethodsTestCase(TestCase):
    def setUp(self):
        self.task_1 = Task.objects.create(title='First Task')
        self.task_2 = Task.objects.create(title='Second Task')

    def test_if_is_possible_to_finish_task(self):
        [self.assertFalse(bool_field) for bool_field in [self.task_1.success, self.task_1.is_finished, self.task_2.success, self.task_1.is_finished]]

        self.task_1.complete()
        self.assertTrue(self.task_1.is_finished)
        self.assertTrue(self.task_1.success)

        self.task_2.cancel()
        self.assertTrue(self.task_2.is_finished)
        self.assertFalse(self.task_2.success)
