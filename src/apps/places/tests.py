from django.test import TestCase

from django.db import connection
from django.urls import reverse
from allauth.socialaccount.models import SocialApp, SocialAccount
from django.core.management import call_command
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model



def config_facebook_provider():
    # change to https
    site = Site.objects.get(id=1)
    site.domain='https://localhost:8000/'
    site.name='https://localhost:8000/'
    site.save()

    # create social app
    sapp = SocialApp(provider='facebook', name='facebook', client_id='1333592763650736',
                     secret='')
    sapp.save()

    sapp.sites.add(1)



# def make_initial_migrations():
#     call_command('makemigrations', 'places')
#     call_command('migrate')


def create_test_user():
    User = get_user_model()
    user = User(username='Dmitry', email='@gmail.com')
    user.set_password(raw_password=None)
    user.save()

    s_account = SocialAccount(user=user, provider='facebook', uid='')
    s_account.save()
    return user

# facebook test user id: 104777861428045 , email: open_uvdpjin_user@tfbnw.net


class MemoryTestCase(TestCase):
    def setUp(self):
        config_facebook_provider()
        self.user = create_test_user()

    def test_user_created(self):
        # s1 = SocialApp.objects.get(id=1)
        # self.assertEqual(s1.provider, 'facebook')
        User = get_user_model()
        u1 = User.objects.filter(username='Dmitry').first()
        self.assertEqual(u1, self.user)

        # correctly added socialapp_cites
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM socialaccount_socialapp_sites WHERE id=1;")
        r = cursor.fetchall()
        print(type(r), flush=True)
        print(r, flush=True)
        self.assertEqual(r[0].site_id, 1)

    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)