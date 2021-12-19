from django.contrib.staticfiles.testing import LiveServerTestCase
from django.contrib.auth.models import User
from django.urls.base import reverse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.keys import Keys


class NavMenuTestCase(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.test_user = User.objects.create_user(username='TestUser', password='TestPass123',
                                                  email='testuser@test.com')

    def tearDown(self):
        self.browser.quit()

    def enter_logged_in(self):
        self.browser.get(self.live_server_url + reverse('login'))
        WebDriverWait(self.browser, 10).until(cond.title_contains('Log In'))

        # log in
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys(self.test_user.username)
        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('TestPass123')
        inputbox.send_keys(Keys.ENTER)
        # wait until redirects to homepage is completed
        WebDriverWait(self.browser, 10).until(cond.title_contains('Homepage'))

    def enter_not_logged_in(self):
        self.browser.get(self.live_server_url)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Homepage'))

    def test_base_html(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1920, 1080)

        # Is the title correct?
        self.assertIn('Family Helper', self.browser.title, msg="Browser title was " + self.browser.title)
        # Is there Nixon's signature?
        nixon_sign = self.browser.find_element_by_class_name('nixons_signature')
        self.assertIn('© Copyrights - Nixon Sparrow', nixon_sign.text)

    # logged in menu links - user supposed to be able to see
    def test_if_logged_in_user_can_see_links_in_navigation_menu_that_should_see(self):
        self.enter_logged_in()

        self.assertTrue(self.browser.find_element_by_id('menu_todo'))
        self.assertTrue(self.browser.find_element_by_id('menu_logout'))

    # logged in menu links - user supposed to be unable to see
    def test_if_logged_in_user_can_see_links_in_navigation_menu_that_should_not_see(self):
        self.enter_logged_in()

        with self.assertRaises(NoSuchElementException):
            self.assertTrue(self.browser.find_element_by_id('menu_log_in'))
        with self.assertRaises(NoSuchElementException):
            self.assertTrue(self.browser.find_element_by_id('menu_register'))

    # not logged in menu links - anonymous user supposed to be able to see
    def test_if_not_logged_in_user_can_see_links_in_navigation_menu_that_should_see(self):
        self.enter_not_logged_in()

        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('menu_todo')
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('menu_logout')

    # not logged in menu links - anonymous user supposed to be able to see
    def test_if_not_logged_in_user_can_see_links_in_navigation_menu_that_should_not_see(self):
        self.enter_not_logged_in()

        self.assertTrue(self.browser.find_element_by_id('menu_log_in'))
        self.assertTrue(self.browser.find_element_by_id('menu_register'))


class LoggingTestCase(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.test_user = User.objects.create_user(username='TestUser', password='TestPass123',
                                                  email='testuser@test.com')

    def tearDown(self):
        self.browser.quit()

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


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()
