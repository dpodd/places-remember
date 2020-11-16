from django.test import TestCase

from django.db import connection
from allauth.socialaccount.models import SocialApp, SocialAccount
from django.core.management import call_command
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model



def oonfig_facebook_provider():
    config_db_tables()

    def config_db_tables():
        # change to https

        # cursor = connection.cursor()
        # cursor.execute(
        #     "UPDATE django_site SET domain='https://localhost:8000/' name='https://localhost:8000/' WHERE id=1")

        site = Site.objects.get(id=1)
        site.domain='https://localhost:8000/'
        site.name='https://localhost:8000/'
        site.save()
        

        # create social app
        sapp = SocialApp(provider='facebook', name='facebook', client_id='',
                         secret='')
        sapp.save()

        sapp.sites.add(1)



def make_initial_migrations():
    call_command('makemigrations', 'places')
    call_command('migrate')


def create_test_user():
    User = get_user_model()
    user = User(username='Dmitry', email='@gmail.com')
    user.set_password(raw_password=None)
    user.save()

    s_account = SocialAccount(user=user, provider='facebook', uid='')
    s_account.save()


class MemoryTestCase(TestCase):
    def setUp(self):
        make_initial_migrations()
        create_test_user()
        config_facebook_provider()

    def test_index_page_healthy(self):
        # res = self.client.get(reverse('index'))
        # assertEqual(res.status_code, 200)
        s1 = SocialApp.objects.get(id=1)
        self.assertEqual(s1.provider, 'facebook')