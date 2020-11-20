from django.test import TestCase, RequestFactory
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import connection

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
import geckodriver_autoinstaller
import time

from .models import Memory
from apps.places.views import profile_view


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
    user = User(username='Open Graph Test User', email='open_uvdpjin_user@tfbnw.net')
    user.set_password(raw_password=None)
    user.save()

    s_account = SocialAccount(user=user, provider='facebook', uid='104777861428045')
    s_account.save()

    sapp = SocialApp.objects.filter(client_id='1333592763650736').first()

    s_token = SocialToken(token = 'EAAS85ULz0rABADvH5EIWRw6qowgqlgapiZBsCIlSqBtAT0wmE9QMMnNA0nZCRdvZBAvnSwv68y0qKud9WXRBr80sexooXIPLOYRY09bmdLF7rP9t7fwjiCzTn2z19gDYaau7BRvfPfXA9Xvl0aQsq8GScKJGKwf3BZCXhaoZCxfwWwiIsQjxTAgCgIedywRtbcu2P5oZCjXXik7woZAiDDR',
                          account_id=user.id,
                          app_id=sapp.id)
    s_token.save()

    return user


def login_through_facebook(driver, url):
    email = 'open_uvdpjin_user@tfbnw.net'
    password = 'HdrIoa'

    driver = driver
    # open index page
    # url = "https://localhost:8000/"
    url = url
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


class UnitTests(TestCase):
    def setUp(self):
        config_facebook_provider()
        self.factory = RequestFactory()

    def test_index_page_opens(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_is_served_for_registered_user(self):
        user = create_test_user()

        # create request to Profile view and attach test user
        request = self.factory.get(reverse("profile"))
        request.user = user

        # process responce
        response = profile_view(request)

        self.assertContains(response, 'У вас нет воспоминаний')
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_is_redirected_to_facebook_login_view(self):
        user = AnonymousUser()

        # create request to Profile view and attach test user
        request = self.factory.get(reverse("profile"))
        request.user = user

        # process responce
        response = profile_view(request)

        time.sleep(2)

        self.assertIn('facebook', response.url)





# class FunctionalTests(StaticLiveServerTestCase):
#     print('Starting Functional Tests'.center(60, '+'))
#     def setUp(self):
#         print(''.center(25, '~'), flush=True)
#         config_facebook_provider()
#
#         start = time.time()
#         geckodriver_autoinstaller.install()  # install geckodriver for Selenium to work with Firefox
#         print('time of geckodriver installation: %s sec' % (time.time() - start), flush=True)
#
#         opts = FirefoxOptions()
#         opts.add_argument("--headless")  # no display mode in container
#         self.driver = webdriver.Firefox(firefox_options=opts)
#         self.driver = login_through_facebook(self.driver, self.live_server_url)
#
#     def test_user_creates_new_memory_and_see_it_in_profile(self):
#         """ New user creates a memory and the memory title gets displayed in the profile page """
#         # assert that new user has no memories
#         print('Current web page title: ', self.driver.title, flush=True)
#         self.assertIn('Профиль', self.driver.title)
#         self.assertIn('У вас нет воспоминаний', self.driver.page_source)
#
#         # press the button to open modal window to create a new memory
#         create_button = self.driver.find_element_by_id('open-modal')
#         create_button.click()
#
#         time.sleep(1)
#
#         # click on the map to place a Marker
#         map = self.driver.find_element_by_id('mapid')
#         ac = ActionChains(self.driver)
#         ac.move_to_element(map).move_by_offset(50, 10).click().perform()
#         lon = self.driver.find_element_by_id('id_lon')
#         lat = self.driver.find_element_by_id('id_lat')
#         print('lon: ', lon.get_attribute('value'), ' ; lat: ', lat.get_attribute('value'))
#
#         # fill out the form fields and click submit button
#         title_field = self.driver.find_element_by_id('id_title')
#         title_field.send_keys('memory 123')
#
#         description_field = self.driver.find_element_by_id('id_description')
#         description_field.send_keys('description 1234567')
#
#         submit_button = self.driver.find_element_by_id('submit-memory')
#         # self.driver.save_screenshot('{}.png'.format(time.time()))
#         submit_button.click()
#         time.sleep(1)
#
#         objs = Memory.objects.all()
#         print("objs: ", objs, flush=True)
#
#
#         html = self.driver.page_source
#         self.assertIn('memory 123', html)
#
#     def tearDowm(self):
#         self.driver.quit()
