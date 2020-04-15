from django.conf import settings
from django.contrib import auth
from som_cas.models import (
	AgRegistration,
	RegistrationChoices,
	Assembly,
)

def member_in_virtual_registry(member):
	registry = AgRegistration.objects.filter(
		member=member,
		assembly__active=True,
		registration_type=RegistrationChoices.VIRTUAL,
	)
	return registry.exists()


def register_member_in_virtual_assembly(member):
	registration = AgRegistration.objects.get()
	if registration.registration_type == RegistrationChoices.INPERSON:
		return None
	return registration
	assembly = Assembly.objects.get(active=True)

	registration, _ = AgRegistration.objects.get_or_create(
		member=member,
		assembly=assembly,
		defaults=dict(
			registration_type=RegistrationChoices.VIRTUAL
		),
	)
	if registration.registration_type == RegistrationChoices.INPERSON:
		return None
	return registration


def get_user(request):
	user = auth.get_user(request)

	if isinstance(user, auth.models.AnonymousUser):
		return user

	if settings.CUSTOM_REGISTRATION_SERVICES in request.GET.get('service', ''):
		return user if member_in_virtual_registry(user) else auth.models.AnonymousUser()

	return user

# vim: noet ts=4 sw=4
