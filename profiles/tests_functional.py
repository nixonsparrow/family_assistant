from django.contrib.staticfiles.testing import LiveServerTestCase
from django.contrib.auth.models import User
from django.urls.base import reverse
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class RegisterTestCase(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.test_user = User.objects.create_user(username='TestUser', password='TestPass123',
                                                  email='testuser@test.com')

    def tearDown(self):
        self.browser.quit()

    def enter_register_credentials(self, username='NewTestUser', email='newuser@email.com',
                                   password1='TestPassword123!@#', password2=None, enter=True):
        if not password2: password2 = password1
        inputbox = self.browser.find_element(By.ID, 'id_username')
        inputbox.send_keys(username)
        inputbox = self.browser.find_element(By.ID, 'id_email')
        inputbox.send_keys(email)
        inputbox = self.browser.find_element(By.ID, 'id_password1')
        inputbox.send_keys(password1)
        inputbox = self.browser.find_element(By.ID, 'id_password2')
        inputbox.send_keys(password2)
        if enter:
            inputbox.send_keys(Keys.ENTER)

    def test_register_and_log_in(self):
        self.browser.get(self.live_server_url)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Homepage'))

        self.browser.find_element(By.ID, 'toggle_button').click()
        self.browser.find_element(By.ID, 'menu_register').click()
        WebDriverWait(self.browser, 10).until(cond.title_contains('Register'))

        # enter new user credentials
        self.enter_register_credentials()
        WebDriverWait(self.browser, 10).until(cond.title_contains('Homepage'))

        # check if new user can login by username and password
        self.browser.find_element(By.ID, 'toggle_button').click()
        self.browser.find_element(By.ID, 'menu_log_in').click()
        WebDriverWait(self.browser, 10).until(cond.title_contains('Log In'))

        # log in with new credentials
        inputbox = self.browser.find_element(By.ID, 'id_username')
        inputbox.send_keys('NewTestUser')
        inputbox = self.browser.find_element(By.ID, 'id_password')
        inputbox.send_keys('TestPassword123!@#')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Homepage'))  # msg = new user probably cannot log in

        # logout
        self.browser.find_element(By.ID, 'toggle_button').click()
        self.browser.find_element(By.ID, 'menu_logout').click()
        WebDriverWait(self.browser, 10).until(cond.title_contains('Logout'))

    def test_register_password_not_equal(self):
        self.browser.get(self.live_server_url + reverse('register'))
        WebDriverWait(self.browser, 10).until(cond.title_contains('Register'))

        with self.assertRaises(NoSuchElementException):
            self.browser.find_element(By.ID, 'error_1_id_password2')

        self.enter_register_credentials(password2='WrongPassword123!@#')
        WebDriverWait(self.browser, 10).until(cond.presence_of_element_located((By.ID, "error_1_id_password2")))

    def test_register_email_not_correct(self):
        self.browser.get(self.live_server_url + reverse('register'))
        WebDriverWait(self.browser, 10).until(cond.title_contains('Register'))

        with self.assertRaises(NoSuchElementException):
            self.browser.find_element(By.ID, 'error_1_id_password2')

        self.enter_register_credentials(email='wrong#email.duh')
        WebDriverWait(self.browser, 10).until(cond.title_contains('Register'))  # no redirect because of wrong email


class UpdateProfileTestCase(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.test_user = User.objects.create_user(username='TestUser', password='TestPass123',
                                                  email='testuser@test.com')

    def tearDown(self):
        self.browser.quit()

    def test_update_profile(self):
        self.browser.get(self.live_server_url + reverse('edit-profile'))
        WebDriverWait(self.browser, 10).until(cond.title_contains('Log In'))

        # log in
        inputbox = self.browser.find_element(By.ID, 'id_username')
        inputbox.send_keys(self.test_user.username)
        inputbox = self.browser.find_element(By.ID, 'id_password')
        inputbox.send_keys('TestPass123')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Edit Profile'))

        # collect old data
        old = [self.test_user.username, self.test_user.email, self.test_user.first_name, self.test_user.last_name]

        # change username, e-mail, first and last name
        inputbox = self.browser.find_element(By.ID, 'id_username')
        inputbox.clear()
        inputbox.send_keys('JohnnyBravo')
        inputbox = self.browser.find_element(By.ID, 'id_email')
        inputbox.clear()
        inputbox.send_keys('johnnybravo@test.com')
        inputbox = self.browser.find_element(By.ID, 'id_first_name')
        inputbox.clear()
        inputbox.send_keys('John')
        inputbox = self.browser.find_element(By.ID, 'id_last_name')
        inputbox.clear()
        inputbox.send_keys('Alpha')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(cond.title_is('Family Helper | Profile'))

        self.browser.get(self.live_server_url + reverse('edit-profile'))
        WebDriverWait(self.browser, 10).until(cond.title_contains('Edit Profile'))

        new = [
            self.browser.find_element(By.ID, 'id_username').get_attribute("value"),
            self.browser.find_element(By.ID, 'id_email').get_attribute("value"),
            self.browser.find_element(By.ID, 'id_first_name').get_attribute("value"),
            self.browser.find_element(By.ID, 'id_last_name').get_attribute("value")
        ]

        for i in range(4):
            self.assertNotEqual(old[i], new[i])


class LoginTestCase(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.test_user = User.objects.create_user(username='TestUser', password='TestPass123',
                                                  email='testuser@test.com')

    def tearDown(self):
        self.browser.quit()

    def test_login_correct_credentials(self):
        self.browser.get(self.live_server_url + reverse('login'))
        WebDriverWait(self.browser, 10).until(cond.title_contains('Log In'))

        inputbox = self.browser.find_element(By.ID, 'id_username')
        inputbox.send_keys(self.test_user.username)
        inputbox = self.browser.find_element(By.ID, 'id_password')
        inputbox.send_keys('TestPass123')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Homepage'))

    def test_login_incorrect_credentials(self):
        self.browser.get(self.live_server_url + reverse('login'))
        WebDriverWait(self.browser, 10).until(cond.title_contains('Log In'))

        inputbox = self.browser.find_element(By.ID, 'id_username')
        inputbox.send_keys(self.test_user.username)
        inputbox = self.browser.find_element(By.ID, 'id_password')
        inputbox.send_keys('TestPass1234')
        inputbox.send_keys(Keys.ENTER)

        with self.assertRaises(TimeoutException):
            WebDriverWait(self.browser, 5).until(cond.title_contains('Homepage'))

        WebDriverWait(self.browser, 10).until(cond.title_contains('Log In'))
