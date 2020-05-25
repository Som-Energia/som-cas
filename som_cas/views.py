from django.shortcuts import render

from mama_cas.views import LoginView

from .forms import SomCasLoginForm

logger = logging.getLogger(__name__)

class SomCasLoginView(LoginView):

    form_class = SomCasLoginForm