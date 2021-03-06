from django.contrib.staticfiles.testing import LiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from todo.models import Task


class CreateNewTask(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.test_user = User.objects.create_user(username='TestUser', password='TestPass123',
                                                  email='testuser@test.com')

    def tearDown(self):
        self.browser.quit()

    def log_in(self):
        self.browser.get(self.live_server_url + reverse('login'))
        WebDriverWait(self.browser, 10).until(cond.title_contains('Log In'))

        # log in
        inputbox = self.browser.find_element(By.ID, 'id_username')
        inputbox.send_keys(self.test_user.username)
        inputbox = self.browser.find_element(By.ID, 'id_password')
        inputbox.send_keys('TestPass123')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Homepage'))

    def test_if_user_can_create_a_new_task(self):
        self.log_in()
        self.browser.get(self.live_server_url + reverse('todo-new-task'))
        WebDriverWait(self.browser, 10).until(cond.title_contains('New Task'))

        # create task
        inputbox = self.browser.find_element(By.ID, 'id_title')
        inputbox.send_keys('Buy a bread')
        inputbox.send_keys(Keys.ENTER)

        # check if test show
        WebDriverWait(self.browser, 10).until(cond.title_contains('Tasks'))
        self.assertIn('Buy a bread', [task.text for task in self.browser.find_elements(By.CLASS_NAME, 'task')])

    def test_if_user_can_create_multiple_new_tasks(self):
        self.log_in()

        task_names = ['Buy some milk', 'Drink 2 litres of water', 'I like pie']

        for task_name in task_names:
            self.browser.get(self.live_server_url + reverse('todo-new-task'))
            WebDriverWait(self.browser, 10).until(cond.title_contains('New Task'))

            # create task
            inputbox = self.browser.find_element(By.ID, 'id_title')
            inputbox.send_keys(task_name)
            inputbox.send_keys(Keys.ENTER)
            WebDriverWait(self.browser, 10).until(cond.title_contains('Tasks'))

        # check if all tasks show
        WebDriverWait(self.browser, 10).until(cond.title_contains('Tasks'))

        for a_task in self.browser.find_elements(By.CLASS_NAME, 'task'):
            self.assertIn(a_task.text, task_names)


class UpdateTask(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.test_user2 = User.objects.create_user(username='TestUser2', password='TestPass123',
                                                  email='testuser@test.com')
        self.task = Task.objects.create(created_by=self.test_user2, title='Buy some milk', content='2 litres of Rice')

    def tearDown(self):
        self.browser.quit()

    def test_if_user_can_update_his_task(self):
        self.browser.get(self.live_server_url + reverse('todo-task-update', kwargs={'pk': self.task.id}))
        WebDriverWait(self.browser, 10).until(cond.title_contains('Log In'))

        # Log in
        inputbox = self.browser.find_element(By.ID, 'id_username')
        inputbox.send_keys('TestUser2')
        inputbox = self.browser.find_element(By.ID, 'id_password')
        inputbox.send_keys('TestPass123')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Buy some milk'))

        # update task
        inputbox = self.browser.find_element(By.ID, 'id_title')
        inputbox.clear()
        inputbox.send_keys('Buy a lot of milk')
        inputbox.send_keys(Keys.ENTER)

        # check if all tasks show
        WebDriverWait(self.browser, 10).until(cond.title_contains('Tasks'))
        self.assertEqual(self.browser.find_element(By.ID, f'task_{self.task.id}').text, 'Buy a lot of milk',
                         msg='Updated task title is not visible on list of tasks.')
        self.browser.get(self.live_server_url + reverse('todo-task-update', kwargs={'pk': self.task.id}))
        WebDriverWait(self.browser, 10).until(cond.title_contains('Buy a lot of milk'),
                      message='Old task title is visible on an update task site.')
