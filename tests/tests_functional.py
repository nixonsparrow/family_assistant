from time import sleep, time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 2


class LoggingTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.test_user = User.objects.create_user(username='TestUser', password='TestPass123',
                                                  email='testuser@test.com')

    def tearDown(self):
        self.browser.quit()

    # old method for perfect timing, left just for history :)
    # def wait_for_site_to_load_the_title(self, title):
    #     start_time = time()
    #     while True:
    #         try:
    #             print(f'Sprawdź!  {title}')
    #             self.assertIn(title, self.browser.title)
    #             print(f'Jest!     {title}')
    #             return
    #         except(AssertionError, WebDriverException) as e:
    #             print(f'Czekaj!   {title}')
    #             if time() - start_time > MAX_WAIT:
    #                 raise e
    #             sleep(0.5)

    def test_base_html(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1920, 1080)

        # Is the title correct?
        self.assertIn('Family Helper', self.browser.title, msg="Browser title was " + self.browser.title)
        # Is there Nixon's signature?
        nixon_sign = self.browser.find_element_by_class_name('nixons_signature')
        self.assertIn('© Copyrights - Nixon Sparrow', nixon_sign.text)

    def test_log_in_and_out(self):
        self.browser.get(self.live_server_url)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Homepage'))

        self.browser.find_element_by_id('toggle_button').click()
        self.browser.find_element_by_id('menu_log_in').click()
        WebDriverWait(self.browser, 10).until(cond.title_contains('Log In'))

        # log in with username
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys(self.test_user.username)
        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('TestPass123')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Homepage'))  # msg = user probably cannot log in with username

        # logout
        self.browser.find_element_by_id('toggle_button').click()
        self.browser.find_element_by_id('menu_logout').click()
        WebDriverWait(self.browser, 10).until(cond.title_contains('Logout'))


class UpdateProfileTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.test_user = User.objects.create_user(username='TestUser', password='TestPass123',
                                                  email='testuser@test.com')

    def tearDown(self):
        self.browser.quit()

    def test_update_profile(self):
        self.browser.get(self.live_server_url + '/profile/edit/')
        WebDriverWait(self.browser, 10).until(cond.title_contains('Log In'))

        # Log in
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys(self.test_user.username)
        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('TestPass123')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Edit Profile'))

        # collect old data
        old = [self.test_user.username, self.test_user.email, self.test_user.first_name, self.test_user.last_name]

        # Change username, e-mail, first and last name
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.clear()
        inputbox.send_keys('JohnnyBravo')
        inputbox = self.browser.find_element_by_id('id_email')
        inputbox.clear()
        inputbox.send_keys('johnnybravo@test.com')
        inputbox = self.browser.find_element_by_id('id_first_name')
        inputbox.clear()
        inputbox.send_keys('John')
        inputbox = self.browser.find_element_by_id('id_last_name')
        inputbox.clear()
        inputbox.send_keys('Alpha')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(cond.title_is('Family Helper | Profile'))

        self.browser.get(self.live_server_url + '/profile/edit/')
        WebDriverWait(self.browser, 10).until(cond.title_contains('Edit Profile'))

        new = [
            self.browser.find_element_by_id('id_username').get_attribute("value"),
            self.browser.find_element_by_id('id_email').get_attribute("value"),
            self.browser.find_element_by_id('id_first_name').get_attribute("value"),
            self.browser.find_element_by_id('id_last_name').get_attribute("value")
        ]

        for x in range(4):
            self.assertNotEqual(old[x], new[x])


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_register_and_log_in(self):
        self.browser.get(self.live_server_url)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Homepage'))

        self.browser.find_element_by_id('toggle_button').click()
        self.browser.find_element_by_id('menu_register').click()
        WebDriverWait(self.browser, 10).until(cond.title_contains('Register'))

        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('TestUser123')

        inputbox = self.browser.find_element_by_id('id_email')
        inputbox.send_keys('TestUser@test.com')

        inputbox = self.browser.find_element_by_id('id_password1')
        inputbox.send_keys('TestPassword123!@#')

        inputbox = self.browser.find_element_by_id('id_password2')
        inputbox.send_keys('TestPassword123!@#')
        inputbox.send_keys(Keys.ENTER)

        WebDriverWait(self.browser, 10).until(cond.title_contains('Homepage'))

        # check if new user can login by username and password
        self.browser.find_element_by_id('toggle_button').click()
        self.browser.find_element_by_id('menu_log_in').click()
        WebDriverWait(self.browser, 10).until(cond.title_contains('Log In'))

        # log in with new credentials
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys('TestUser123')
        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('TestPassword123!@#')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Homepage'))  # msg = new user probably cannot log in

        # logout
        self.browser.find_element_by_id('toggle_button').click()
        self.browser.find_element_by_id('menu_logout').click()
        WebDriverWait(self.browser, 10).until(cond.title_contains('Logout'))
