from django.test import TestCase, Client


class BaseTestCase(TestCase):
    """
    login as ordinary company user
    """
    fixtures = ['tests.json']

    def setUp(self):
        self.client = Client()
        self._username = "john"
        self._password = "123"
        self.login = self.client.login(username=self._username, password=self._password)
        print self.login
        # check login
        self.assertEqual(self.login, True)
