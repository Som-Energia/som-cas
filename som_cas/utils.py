from django.conf import settings
from django.contrib import auth
from som_cas.models import (
	AgRegistration,
	RegistrationChoices,
	Assembly,
	register_member_in_virtual_assembly,
)



def get_user(request):
	user = auth.get_user(request)

	if isinstance(user, auth.models.AnonymousUser):
		return user

	if settings.CUSTOM_REGISTRATION_SERVICES in request.GET.get('service', ''):
		if user.isVirtualRegisteredInActiveAssembly():
			return user
		return auth.models.AnonymousUser()

	return user

# vim: noet ts=4 sw=4
