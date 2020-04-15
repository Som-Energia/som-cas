from django.test import Client, TestCase
from som_cas.backends import SocisBackend


class TestSocisBackend(TestCase):

    def setUp(self):
        self.c = Client()

    def test_authenticate(self):
        pass

    def test_get_user(self):
        pass

# vim: noet sw=4 ts=4
