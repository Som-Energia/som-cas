from mama_cas.views import LoginView

from .forms import SomCasLoginForm


class SomCasLoginView(LoginView):

    form_class = SomCasLoginForm