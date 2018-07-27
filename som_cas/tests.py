from django.test import Client, TestCase

from som_cas.backends import SocisBackend
from som_cas.views import get_ticket


class TestSocisBackend(TestCase):

    def setUp(self):
        self.c = Client()

    def test_authenticate(self):
        pass

    def test_get_user(self):
        pass


class TestLoginView(TestCase):

    TICKET = {
        'ticket': 'ST-1532705021-WYFD6L8kTjXRxhDTpaJmDVTqVElcx9Gu'
    }

    def setUp(self):
        self.c = Client()

    def test_get_ticket(self):
        URL = 'https://api.somenergia.coop?ticket=ST-1532705021-WYFD6L8kTjXRxhDTpaJmDVTqVElcx9Gu'

        ticket = get_ticket(URL)

        self.assertDictEqual(ticket, self.TICKET)
