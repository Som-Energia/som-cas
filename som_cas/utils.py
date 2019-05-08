from django.conf import settings
from django.contrib import auth


from som_cas.backends import member_in_registry


def get_user(request):
	user = auth.get_user(request)

	if isinstance(user, auth.models.AnonymousUser):
		return user

	if settings.CUSTOM_REGISTRATION_SERVICES in request.GET.get('service', ''):
		return user if member_in_registry(user) else auth.models.AnonymousUser()

	return user
