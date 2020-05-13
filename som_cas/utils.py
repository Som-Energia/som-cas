from config.settings.base import BCC

from django.conf import settings
from django.contrib import auth
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _, override


def get_user(request):
	user = auth.get_user(request)

	if isinstance(user, auth.models.AnonymousUser):
		return user

	if settings.CUSTOM_REGISTRATION_SERVICES in request.GET.get('service', ''):
		if user.isVirtualRegisteredInActiveAssembly():
			return user
		return auth.models.AnonymousUser()

	return user

def send_confirmation_email(user, email_template):
	from som_cas.models import AgRegistration

	user_registration = AgRegistration.objects.filter(
		member=user,
		assembly__active=True,
		registration_email_sent=False
	)
	if user_registration:
		with override(user.lang):
			if user:
				msg = EmailMessage(
					_('Confirmació d’Inscripció a la Assemblea'),
					render_to_string(email_template),
					'',
					[user.email],
					BCC,
				)
				msg.content_subtype = "html"
				msg.send()

# vim: noet ts=4 sw=4
