import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db import connections

logger = logging.getLogger(__name__)

UserModel = get_user_model()


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
            user = self._fetch_user_from_db(socis_by_username.format(username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if check_password(password, user.password):
                return user

        return None

    def get_user(self, user_id):
        socis_by_id = self.BASE_QUERY_SOCIS.format(
            conditions='id = \'{}\''
        )
        try:
            user = self.__fetch_user_from_db(socis_by_id.format(user_id))
        except UserModel.DoesNotExist:
            return None
        else:
            return user

    def _fetch_user_from_db(self, user_query):
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
    pass
