from todo.models import Task
from django.test import TestCase, Client


class HomePageTestCase(TestCase):
    def test_uses_proper_template(self):
        response = self.client.get('/')

        # can we see proper template?
        self.assertTemplateUsed(response, 'homepage.html')


class ToDoTaskListTestCase(TestCase):
    def setUp(self):
        self.task_1 = Task.objects.create(title='First Task')
        self.task_2 = Task.objects.create(title='Second Task')

    def test_uses_proper_template(self):
        response = self.client.get('/todo/')

        # can we see proper template?
        self.assertTemplateUsed(response, 'todo/task_list.html')

    def test_if_shows_tasks(self):
        response = self.client.get('/todo/')

        self.assertContains(response, self.task_1.title)
        self.assertContains(response, self.task_2.title)


class ToDoNewTaskTestCase(TestCase):

    def test_uses_proper_template(self):
        response = self.client.get('/todo/new')

        # can we see proper template?
        self.assertTemplateUsed(response, 'todo/task_form.html')

    def test_new_task_can_save_a_POST_request(self):
        self.client.post('/todo/new', data={'title': 'Test Task'})

        # have we added a new object to the database?
        self.assertEqual(Task.objects.count(), 1, msg='Task was NOT added to the database.')
        new_item = Task.objects.first()
        self.assertEqual(new_item.title, 'Test Task', msg='Wrong task was added to the database.')
        self.assertFalse(new_item.is_finished, msg='Task was created as completed.')

    def test_redirects_after_POST(self):
        response = self.client.post('/todo/new', data={'title': 'Test Task'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/todo/')


class TasksMethodsTestCase(TestCase):
    def setUp(self):
        self.task_1 = Task.objects.create(title='First Task')
        self.task_2 = Task.objects.create(title='Second Task')

    def test_if_is_possible_to_finish_task(self):
        self.assertFalse(self.task_1.is_finished)
        self.task_1.finish()
        self.assertTrue(self.task_1.is_finished)
