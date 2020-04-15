from django.test import Client, TestCase
from som_cas.backends import SocisBackend
from som_cas.utils import (
	member_in_virtual_registry,
	register_member_in_virtual_assembly,
)
from som_cas.models import (
	SomUser,
	Assembly,
	AgRegistration,
	RegistrationChoices,
)

class TestUtils(TestCase):

	def setUp(self):
		self.user = SomUser(
			username="Pin Pam",
			www_soci=666,
		)
		self.user.save()

		self.other_user = SomUser(
			username="Pan Pim",
			www_soci=999,
		)
		self.other_user.save()

		self.old_assembly = Assembly(
			name='Assamblea 2019',
			date='2019-03-20',
			active=False,
		)
		self.old_assembly.save()

		self.assembly = Assembly(
			name='Assamblea 2020',
			date='2020-03-20',
			active=True,
		)
		self.assembly.save()

	def test__member_in_virtual_registry__noRegistration(self):
		self.assertEqual(member_in_virtual_registry(self.user), False)

	def test__member_in_virtual_registry__whenYes(self):
		registration = AgRegistration(
			member=self.user,
			assembly=self.assembly,
			registration_type=RegistrationChoices.VIRTUAL,
		)
		registration.save()
		self.assertEqual(member_in_virtual_registry(self.user), True)

	def test__member_in_virtual_registry__otherUserRegistered(self):
		registration = AgRegistration(
			member=self.other_user, # This changes
			assembly=self.assembly,
			registration_type=RegistrationChoices.VIRTUAL,
		)
		registration.save()
		self.assertEqual(member_in_virtual_registry(self.user), False)

	def test__member_in_virtual_registry__inOlderAssembly(self):
		registration = AgRegistration(
			member=self.user,
			assembly=self.old_assembly,
			registration_type=RegistrationChoices.VIRTUAL,
		)
		registration.save()
		self.assertEqual(member_in_virtual_registry(self.user), False)


class TestSocisBackend(TestCase):

    def setUp(self):
        self.c = Client()

    def test_authenticate(self):
        pass

    def test_get_user(self):
        pass

# vim: noet sw=4 ts=4
