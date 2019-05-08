from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


class SomUser(AbstractUser):
    """
    User definition for our autentication service
    """

    lang = models.CharField(max_length=10, blank=True, null=True)

    www_phone = models.CharField(max_length=64, blank=True, null=True)

    www_mobile = models.CharField(max_length=64, blank=True, null=True)

    www_soci = models.IntegerField(blank=True, null=True)

    def __repr__(self):
        return '<SomUser(username={}, soci={})>'.format(
            self.username, self.www_soci
        )

    def __str__(self):
        return self.__repr__()


class AgRegistration(models.Model):

    registration_file = models.FileField(
        upload_to=settings.UPLOAD_DIR,
        verbose_name=_('Registration file'),
        help_text=_('File in json format with all register members '
                       'for the virtual assambley')
    )


# class AssambleyRegister(models.Model):

#     member = models.ForeignKey(
#         SomUser,
#         on_delete=models.CASCADE,
#         related_name='assambley_register'
#     )

#     registration_code = models.CharField(max_length=64, blank=True, null=True)

#     assambley_year = models.DateField()
