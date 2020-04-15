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

	def create(self, clss, **kwds):
		obj = clss(**kwds)
		obj.save()
		return obj

	def setUp(self):
		self.user = self.create(SomUser,
			username="Pin Pam",
			www_soci=666,
		)

		self.other_user = self.create(SomUser,
			username="Pan Pim",
			www_soci=999,
		)

		self.old_assembly = self.create(Assembly,
			name='Assamblea 2019',
			date='2019-03-20',
			active=False,
		)

		self.assembly = self.create(Assembly,
			name='Assamblea 2020',
			date='2020-03-20',
			active=True,
		)

	def test__member_in_virtual_registry__noRegistration(self):
		self.assertEqual(member_in_virtual_registry(self.user), False)

	def test__member_in_virtual_registry__whenYes(self):
		registration = self.create(AgRegistration,
			member=self.user,
			assembly=self.assembly,
			registration_type=RegistrationChoices.VIRTUAL,
		)
		self.assertEqual(member_in_virtual_registry(self.user), True)

	def test__member_in_virtual_registry__otherUserRegistered(self):
		registration = self.create(AgRegistration,
			member=self.other_user, # This changes
			assembly=self.assembly,
			registration_type=RegistrationChoices.VIRTUAL,
		)
		self.assertEqual(member_in_virtual_registry(self.user), False)

	def test__member_in_virtual_registry__inOlderAssembly(self):
		registration = self.create(AgRegistration,
			member=self.user,
			assembly=self.old_assembly,
			registration_type=RegistrationChoices.VIRTUAL,
		)
		self.assertEqual(member_in_virtual_registry(self.user), False)

	def test__member_in_virtual_registry__inPerson(self):
		registration = self.create(AgRegistration,
			member=self.user,
			assembly=self.assembly,
			registration_type=RegistrationChoices.INPERSON,
		)
		self.assertEqual(member_in_virtual_registry(self.user), False)

	def test__register_member_in_virtual_assembly__inPerson(self):
		registration = self.create(AgRegistration,
			member=self.user,
			assembly=self.assembly,
			registration_type=RegistrationChoices.INPERSON,
		)
		result = register_member_in_virtual_assembly(self.user)
		self.assertEqual(result, None)
		self.assertEqual(list(AgRegistration.objects.all()), [registration])

	def test__register_member_in_virtual_assembly__virtual(self):
		registration = self.create(AgRegistration,
			member=self.user,
			assembly=self.assembly,
			registration_type=RegistrationChoices.VIRTUAL,
		)
		result = register_member_in_virtual_assembly(self.user)
		self.assertEqual(result, registration)
		self.assertEqual(list(AgRegistration.objects.all()), [registration])

	def test__register_member_in_virtual_assembly__notRegistered(self):
		result = register_member_in_virtual_assembly(self.user)
		self.assertTrue(result)
		self.assertEqual(list(AgRegistration.objects.all()), [result])
		self.assertEqual(result.registration_type, RegistrationChoices.VIRTUAL)


class TestSocisBackend(TestCase):

    def setUp(self):
        self.c = Client()

    def test_authenticate(self):
        pass

    def test_get_user(self):
        pass

# vim: noet sw=4 ts=4
