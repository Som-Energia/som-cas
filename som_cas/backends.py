import logging
import re

from django.db import connections
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import check_password

logger = logging.getLogger(__name__)

UserModel = get_user_model()


class SomUserMixin(object):
    """
    Mixing class to obtain a user from 'users_db' DATABASE
    """
    BASE_SOMUSER_QUERY = 'select * from som_users where {conditions};'

    def fetch_user_from_db(self, username):
        """
        Fetch a user from database defined in 'users_db' DATABASES settings.
        """

        client_by_username = self.BASE_SOMUSER_QUERY.format(
            conditions='username = %s'
        )
        try:
            with connections['users_db'].cursor() as cursor:
                cursor.execute(client_by_username, (username, ))
                columns = [col.name for col in cursor.description]
                user = cursor.fetchone()
        except Exception as e:
            msg = "An error occured executing '%s': %s"
            logger.error(msg, client_by_username, e)
            raise e
        else:
            if user:
                raw_user = dict(zip(columns, user))
                return UserModel(**raw_user)
            else:
                return UserModel.objects.get(username=username)


class SomServiceMixin(object):
    """
    Mixing class to determinate from which service a user is trying to access
    """

    def get_service(self, request):
        return request.GET.get('service', None)


class SomGroupsMixin():

    GROUP_NAME = ''

    def add_group(self, user):
        try:
            g = Group.objects.get(name=self.GROUP_NAME)
        except Exception:
            msg = 'Group %s does not exists, it will not be added'
            logger.warning(msg, self.GROUP_NAME)
        else:
            user.groups.add(g)


class SocisBackend(SomUserMixin, SomGroupsMixin):
    """
    Backend athentication for SomEnergia socis
    """

    GROUP_NAME = 'socis'

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = self.fetch_user_from_db(username.upper().strip())
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            return self.validate_user(user, password)

        return None

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None
        else:
            return user if self.user_can_authenticate(user) else None

    def validate_user(self, user, password, **kwargs):
        if check_password(password, user.password) and \
           self.user_can_authenticate(user):
            user.save()
            self.add_group(user)
            return user

        return None

    def user_can_authenticate(self, user):
        return user.is_soci and getattr(user, 'is_active', False)


class ClientsBackend(SomUserMixin, SomServiceMixin, SomGroupsMixin):
    """
    Backend athentication for general clients in Som Energia
    """

    CLIENT_SERVICES_ALLOWED = getattr(settings, 'CLIENT_SERVICES_ALLOWED', [])

    GROUP_NAME = 'clients'

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = self.fetch_user_from_db(username.upper().strip())
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            return self.validate_user(user, password, request=request)

        return None

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None
        else:
            return user if self.user_can_authenticate(user) else None

    def validate_user(self, user, password, **kwargs):

        if not kwargs.get('request', False):
            return None

        service = self.get_service(kwargs['request'])
        logger.debug('Service: %s', service)

        if check_password(password, user.password) and \
           self.user_can_authenticate(user, service=service):
            user.save()
            self.add_group(user)
            return user

        return None

    def user_can_authenticate(self, user, **kwargs):
        is_allowed_service = True
        service = kwargs.get('service')
        if service:
            is_allowed_service = self._check_service(service)

        return getattr(user, 'is_active', False) and is_allowed_service

    def _check_service(self, service):
        for allowed_service in self.CLIENT_SERVICES_ALLOWED:
            if re.match(allowed_service, service):
                return True

        return False


class SomAuthBackend(SomUserMixin, ModelBackend):
    """
    Base class for Authentication backends in Som Energia
    """

    BACKENDS = [
        ('socis', SocisBackend()),
        ('clients', ClientsBackend())
    ]

    def authenticate(self, request, username=None, password=None, **kwargs):
        args = (request, username, password, )
        try:
            user = self.fetch_user_from_db(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            backend = self._get_user_backend(user)
            logger.debug('User %s; backend %s', user, backend)
            if backend:
                return backend.validate_user(user, password, request=request)

            for group, backend in self.BACKENDS:
                user_validated = backend.validate_user(user, password, request=request)
                if user_validated:
                    return user_validated

            return super().authenticate(*args, **kwargs)

        return None

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            user = None
        else:
            backend = self._get_user_backend(user)
            logger.debug('Backend %s', backend)
            return backend.get_user(user_id) \
                if backend else super().get_user(user_id)

        return user

    def _get_user_backend(self, user):
        if user.groups.first():
            for group, backend in self.BACKENDS:
                if group == user.groups.first().name:
                    return backend

        return None
