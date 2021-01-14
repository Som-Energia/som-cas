from mama_cas.views import LoginView

from .forms import SomCasLoginForm


class SomCasLoginView(LoginView):

    template_name = 'som_cas/login.html'
    form_class = SomCasLoginForm
