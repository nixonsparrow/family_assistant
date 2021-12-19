from django.contrib.staticfiles.testing import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.keys import Keys


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
        self.browser.get(self.live_server_url + '/profile/edit/')
        WebDriverWait(self.browser, 10).until(cond.title_contains('Log In'))

        # log in
        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys(self.test_user.username)
        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys('TestPass123')
        inputbox.send_keys(Keys.ENTER)
        WebDriverWait(self.browser, 10).until(cond.title_contains('Edit Profile'))

        # collect old data
        old = [self.test_user.username, self.test_user.email, self.test_user.first_name, self.test_user.last_name]

        # change username, e-mail, first and last name
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

        for i in range(4):
            self.assertNotEqual(old[i], new[i])
