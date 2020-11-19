from django.test import TestCase
from django.urls import reverse
from allauth.socialaccount.models import SocialApp, SocialAccount
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.db import connection

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
import geckodriver_autoinstaller
import time

from .models import Memory



def config_facebook_provider():
    # change to https
    site = Site.objects.get(id=1)
    site.domain = 'https://localhost:8000/'
    site.name = 'https://localhost:8000/'
    site.save()

    # create social app
    sapp = SocialApp(provider='facebook', name='facebook', client_id='1333592763650736',
                     secret='63d8bda4b4960995f2cd83f187384f31')
    sapp.save()

    sapp.sites.add(site)


def create_test_user():
    User = get_user_model()
    user = User(username='Dmitry', email='@gmail.com')
    user.set_password(raw_password=None)
    user.save()

    s_account = SocialAccount(user=user, provider='facebook', uid='')
    s_account.save()
    return user


def login_through_facebook(driver):
    email = 'open_uvdpjin_user@tfbnw.net'
    password = 'HdrIoa'

    driver = driver
    # open index page
    url = "https://localhost:8000/"
    print("login_through_facebook__url: ", url, flush=True)
    driver.get(url)
    time.sleep(1)
    print("index page title: ", driver.title, flush=True)
    signin_button = driver.find_element_by_id('sign_in')
    signin_button.click()

    time.sleep(5)

    # facebook login page opens
    print("login page title: ", driver.title, flush=True)
    email_element = driver.find_element_by_id('email')
    email_element.send_keys(email)

    password_element = driver.find_element_by_id('pass')
    password_element.send_keys(password)

    login_button = driver.find_element_by_id('loginbutton')
    login_button.click()

    time.sleep(3)
    if "Facebook" in driver.title:
        confirm_button = driver.find_element_by_name('__CONFIRM__')
        confirm_button.click()

    # profile page should be displayed if success
    print("profile page title: ", driver.title, flush=True)
    return driver


class BasicTestCase(TestCase):
    def setUp(self):
        config_facebook_provider()

    def test_index_page_opens(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class FacebookUserTestCase(TestCase):
    print('Starting FacebookUserTestCase'.center(60, '+'))
    def setUp(self):
        print(''.center(25, '~'), flush=True)
        config_facebook_provider()

        start = time.time()
        geckodriver_autoinstaller.install()  # install geckodriver for Selenium to work with Firefox
        print('time of geckodriver installation: %s sec' % (time.time() - start), flush=True)

        opts = FirefoxOptions()
        opts.add_argument("--headless")  # no display mode in container
        self.driver = webdriver.Firefox(firefox_options=opts)
        self.driver = login_through_facebook(self.driver)

    def test_profile_page_rendered_for_user(self):
        """ Profile page with no memories list is displayed for a new user """
        print('Current web page title: ', self.driver.title, flush=True)
        self.assertIn('Профиль', self.driver.title)
        self.assertIn('У вас нет воспоминаний', self.driver.page_source)

    def test_user_creates_new_memory_and_see_it_in_profile(self):
        """ New user creates a memory and the memory title gets displayed in the profile page """
        print('Current web page title: ', self.driver.title, flush=True)
        # press the button to open modal window to create a new memory
        create_button = self.driver.find_element_by_id('open-modal')
        create_button.click()

        time.sleep(1)

        # click on the map to place a Marker
        map = self.driver.find_element_by_id('mapid')
        ac = ActionChains(self.driver)
        ac.move_to_element(map).move_by_offset(50, 10).click().perform()
        lon = self.driver.find_element_by_id('id_lon')
        lat = self.driver.find_element_by_id('id_lat')
        print('lon: ', lon.get_attribute('value'), ' ; lat: ', lat.get_attribute('value'))

        # fill out the form fields and click submit button
        title_field = self.driver.find_element_by_id('id_title')
        title_field.send_keys('memory 123')

        description_field = self.driver.find_element_by_id('id_description')
        description_field.send_keys('description 1234567')

        submit_button = self.driver.find_element_by_id('submit-memory')
        submit_button.click()
        time.sleep(1)


        # obj = Memory.objects.latest('created')
        obj = Memory.objects.get(id=1)
        #obj = Memory.objects.all()

        self.assertEqual('memory 123', obj)

        html = self.driver.page_source
        print(html, flush=True)
        self.assertIn('memory_1', html)

    def tearDowm(self):
        self.driver.quit()
        cursor = connection.cursor()
        cursor.execute("DROP DATABASE test_postgres;")
        cursor.commit()







