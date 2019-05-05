import logging
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db import connections

from som_cas.models import AgRegistration

logger = logging.getLogger(__name__)

UserModel = get_user_model()


def member_in_registry(member):
    registry = AgRegistration.objects.first()
    registered_members = json.loads(
        registry.registration_file.read()
    )

    logger.debug(
        'Checking member %s in %s registry',
        member.username, registry.registration_file.name
    )
    for register in registered_members:
        for _, nif in register['registration_form_answers'].items():
            if member.username.upper() == nif.upper():
                return True
    return False


class SocisBackend(object):
    """
    Backend athentication for SomEnergia socis
    """

    BASE_QUERY_SOCIS = 'select * from som_users where {conditions};'

    def authenticate(self, request, username=None, password=None, **kwargs):
        socis_by_username = self.BASE_QUERY_SOCIS.format(
            conditions='username = \'{}\''
        )
        try:
            user = self._fetch_user_from_db(
                socis_by_username.format(username.upper())
            )
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if check_password(password, user.password) and self.is_soci(user):
                logger.debug(request.GET.get('service'))
                if settings.CUSTOM_REGISTRATION_SERVICES in request.GET.get('service', ''):
                    if member_in_registry(user):
                        user.save()
                        return user
                    return None

                user.save()
                return user

        return None

    def get_user(self, user_id):

        logger.debug('Getting user' + '*' * 30)

        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None
        else:
            return user if self.is_soci(user) else None

    def is_soci(self, user):
        return user.www_soci is not None

    def _fetch_user_from_db(self, user_query):
        """
        Fetch a user from database defined in 'users_db' DATABASES settings.
        """
        try:
            with connections['users_db'].cursor() as cursor:
                cursor.execute(user_query)
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
            else:
                raise UserModel.DoesNotExist()



class ClientesBackend(object):
    """
     Backend athentication for general clients in Som Energia
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        pass

    def get_user(self, user_id):
        pass
