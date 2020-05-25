import logging

from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from mama_cas.forms import LoginForm
from .backends import RegisterException

logger = logging.getLogger(__name__)


class SomCasLoginForm(LoginForm):
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                self.user = authenticate(request=self.request, username=username, password=password)
            except RegisterException:
                logger.exception("A presential user %s tried to register into virtual assembly", username)
                error_msg = _('You are already registered as presential voter')
                raise forms.ValidationError(error_msg)
            except Exception:
                logger.exception("Error authenticating %s" % username)
                error_msg = _('Internal error while authenticating user')
                raise forms.ValidationError(error_msg)

            if self.user is None:
                logger.warning("Failed authentication for %s" % username)
                error_msg = _('The username or password is not correct')
                raise forms.ValidationError(error_msg)
            else:
                if not self.user.is_active:
                    logger.warning("User account %s is disabled" % username)
                    error_msg = _('This user account is disabled')
                    raise forms.ValidationError(error_msg)

        return self.cleaned_data