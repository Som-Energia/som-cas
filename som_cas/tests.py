from django.test import Client, TestCase
from som_cas.backends import SocisBackend
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
			username="Alice",
			www_soci=666,
		)

		self.other_user = self.create(SomUser,
			username="Bob",
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

	def test__isVirtualRegisteredInActiveAssembly__noRegistration(self):
		self.assertEqual(self.user.isVirtualRegisteredInActiveAssembly(), False)

	def test__isVirtualRegisteredInActiveAssembly__whenYes(self):
		registration = self.create(AgRegistration,
			member=self.user,
			assembly=self.assembly,
			registration_type=RegistrationChoices.VIRTUAL,
		)
		self.assertEqual(self.user.isVirtualRegisteredInActiveAssembly(), True)

	def test__isVirtualRegisteredInActiveAssembly__otherUserRegistered(self):
		registration = self.create(AgRegistration,
			member=self.other_user, # This changes
			assembly=self.assembly,
			registration_type=RegistrationChoices.VIRTUAL,
		)
		self.assertEqual(self.user.isVirtualRegisteredInActiveAssembly(), False)

	def test__isVirtualRegisteredInActiveAssembly__inOlderAssembly(self):
		registration = self.create(AgRegistration,
			member=self.user,
			assembly=self.old_assembly, # This changes
			registration_type=RegistrationChoices.VIRTUAL,
		)
		self.assertEqual(self.user.isVirtualRegisteredInActiveAssembly(), False)

	def test__isVirtualRegisteredInActiveAssembly__inPerson(self):
		registration = self.create(AgRegistration,
			member=self.user,
			assembly=self.assembly,
			registration_type=RegistrationChoices.INPERSON, # This changes
		)
		self.assertEqual(self.user.isVirtualRegisteredInActiveAssembly(), False)

	def test__registerInVirtualAssembly__inPerson(self):
		registration = self.create(AgRegistration,
			member=self.user,
			assembly=self.assembly,
			registration_type=RegistrationChoices.INPERSON,
		)
		result = self.user.registerInVirtualAssembly()
		self.assertEqual(result, None)
		self.assertEqual(list(AgRegistration.objects.all()), [registration])

	def test__registerInVirtualAssembly__virtual(self):
		registration = self.create(AgRegistration,
			member=self.user,
			assembly=self.assembly,
			registration_type=RegistrationChoices.VIRTUAL,
		)
		result = self.user.registerInVirtualAssembly()
		self.assertEqual(result, registration)
		self.assertEqual(list(AgRegistration.objects.all()), [registration])

	def test__registerInVirtualAssembly__notRegistered(self):
		result = self.user.registerInVirtualAssembly()
		self.assertTrue(result)
		self.assertEqual(list(AgRegistration.objects.all()), [result])
		self.assertEqual(result.member, self.user)
		self.assertEqual(result.assembly, self.assembly)
		self.assertEqual(result.registration_type, RegistrationChoices.VIRTUAL)

	def test__registerInVirtualAssembly__olderAssembly(self):
		registration = self.create(AgRegistration,
			member=self.user,
			assembly=self.old_assembly, # This changes
			registration_type=RegistrationChoices.VIRTUAL,
		)
		result = self.user.registerInVirtualAssembly()
		self.assertEqual(list(AgRegistration.objects.all()), [registration, result])
		self.assertEqual(result.member, self.user)
		self.assertEqual(result.assembly, self.assembly)
		self.assertEqual(result.registration_type, RegistrationChoices.VIRTUAL)

	def test__registerInVirtualAssembly__otherPersonRegistered(self):
		registration = self.create(AgRegistration,
			member=self.other_user, # This changes
			assembly=self.assembly,
			registration_type=RegistrationChoices.VIRTUAL,
		)
		result = self.user.registerInVirtualAssembly()
		self.assertEqual(result.member, self.user)
		self.assertEqual(result.assembly, self.assembly)
		self.assertEqual(result.registration_type, RegistrationChoices.VIRTUAL)
		self.assertEqual(list(AgRegistration.objects.all()), [registration, result])

	def test__registerInVirtualAssembly__noActiveAssembly(self):
		self.assembly.active=False
		self.assembly.save()
		result = self.user.registerInVirtualAssembly()
		self.assertEqual(result, None)
		self.assertEqual(list(AgRegistration.objects.all()), [])



class TestSocisBackend(TestCase):

    def setUp(self):
        self.c = Client()

    def test_authenticate(self):
        pass

    def test_get_user(self):
        pass

# vim: noet sw=4 ts=4
