import logging

from django.db import connections
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

logger = logging.getLogger(__name__)

UserModel = get_user_model()


class SomAuthBackend(object):
    """
    Base class for Authentication backends in Som Energia
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        raise NotImplemented

    def get_user(self, user_id):
        raise NotImplemented


class SomUserMixin(object):
    """
    Mixing class for obtain a ?service=https%3A%2F%2Fparticipa.somenergia.coop:8080user from 'users_db' DATABASE
    """

    def fetch_user_from_db(self, user_query, *query_args):
        """
        Fetch a user from database defined in 'users_db' DATABASES settings.
        """
        try:
            with connections['users_db'].cursor() as cursor:
                cursor.execute(user_query, query_args)
                columns = [col.name for col in cursor.description]
                user = cursor.fetchone()
        except Exception as e:
            msg = "An error occured executing '%s': %s"
            logger.error(msg, user_query, e)
            raise e
        else:
            if user:
                raw_user = dict(zip(columns, user))
                return UserModel(**raw_user)

            raise UserModel.DoesNotExist()


class SomServiceMixin(object):
    """
    Mixing class to determinate from which service are trying to access
    """

    def get_service(self, request):
        method = getattr(request, request.method, request.GET)

        logger.debug(request.path_info)

        return method.get('service', '')


class SocisBackend(SomAuthBackend, SomUserMixin):
    """
    Backend athentication for SomEnergia socis
    """

    BASE_QUERY_SOCIS = getattr(
        settings, 'SOCIS_QUERY', 'select * from auth_user where {conditions};'
    )

    def authenticate(self, request, username=None, password=None, **kwargs):
        socis_by_username = self.BASE_QUERY_SOCIS.format(
            conditions='username = %s'
        )
        try:
            user = self.fetch_user_from_db(
                socis_by_username, username.upper()
            )
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if check_password(password, user.password) and user.is_soci:
                user.save()
                return user

        return None

    def get_user(self, user_id):
        try:
            user = UserModel.objectSomServiceMixins.get(id=user_id)
        except UserModel.DoesNotExist:
            return None
        else:
            return user if user.is_soci else None


class ClientsBackend(SomAuthBackend, SomUserMixin, SomServiceMixin):
    """
     Backend athentication for general clients in Som Energia
    """

    BASE_QUERY_CLIENTS = getattr(
        settings, 'CLIENTS_QUERY', 'select * from auth_user where {conditions};'
    )

    SERVICES_ALLOWED = ['']

    def authenticate(self, request, username=None, password=None, **kwargs):
        clients_by_username = self.BASE_QUERY_CLIENTS.format(
            conditions='username = %s'
        )
        try:
            user = self.fetch_user_from_db(
                clients_by_username, username.upper()
            )
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            self.service = self.get_service(request)
            logger.debug(self.service)
            if check_password(password, user.password) and self._check_service(self.service):
                user.save()
                return user

        return None

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None
        else:
            return user

    def _check_service(self, service):
        return service in self.SERVICES_ALLOWED
