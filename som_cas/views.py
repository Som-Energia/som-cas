import logging

from django.contrib.auth import login

from mama_cas.views import LoginView
from mama_cas.models import ServiceTicket
from mama_cas.utils import redirect

logger = logging.getLogger('som_cas')


class SomLoginView(LoginView):

    def form_valid(self, form):
        login(self.request, form.user, 'som_cas.backends.SomAuthBackend')
        logger.info("Single sign-on session started for %s" % form.user)

        if form.cleaned_data.get('warn'):
            self.request.session['warn'] = True

        service = self.request.GET.get('service')
        if service:
            st = ServiceTicket.objects.create_ticket(
                service=service, user=self.request.user, primary=True
            )
            return redirect(service, params={'ticket': st.ticket})
        return redirect('cas_login')
