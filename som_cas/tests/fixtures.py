import pytest
from erppeek import Client
from django.db import connections
from django.contrib.auth import get_user_model

from som_cas.middleware import _set_erp_connection
from . import factories


@pytest.fixture(scope='function')
def erp_con(settings):
    return _set_erp_connection(lambda self: Client(**settings.ERP))


@pytest.fixture(scope='function')
def mock_madrid_address_codes(monkeypatch):
    address_codes = ('13', '28', '28791')
    monkeypatch.setattr(factories.SomUser, "address_codes", address_codes)


@pytest.fixture(autouse=True)
def set_debug_when_testing(settings):
    settings.DEBUG = True


@pytest.fixture(scope='function')
def local_group():
    factories.BaixMontsenyFactory.create()
    factories.AlmeriaFactory.create()
    factories.CMadridFactory.create()
    factories.GironaFactory.create()


@pytest.fixture(scope='function')
def assemblies():
    factories.ActiveGeneralAssamblyFactory.create()
    factories.InactiveGenerealAssamblyFactory.create()
    factories.ActiveLocalGroupAssemblyFactory.create()
    factories.InactiveGeneralAssemblyFactory.create()


@pytest.fixture(scope='function')
def active_general_assembly():
    return factories.ActiveGeneralAssemblyFactory.create()


@pytest.fixture(scope='function')
def inactive_general_assembly():
    return factories.InactiveGeneralAssemblyFactory.create()


@pytest.fixture(scope='function')
def old_register_in_general_assembly():
    return factories.OldAgRegistrationFactory.create()


@pytest.fixture(scope='function')
def active_madridlocalgroup_assembly():
    return factories.ActiveMadridLocalGroupAssemblyFactory.create()


@pytest.fixture(scope='function')
def active_baixmontsenylocalgroup_assembly():
    return factories.ActiveBaixMontsenyLocalGroupAssemblyFactory.create()


@pytest.fixture(scope='function')
def user():
    return factories.SomUserFactory.build()


@pytest.fixture(scope='function')
def members():
    alice = factories.AliceSomUserFactory.create()
    alice.set_password('1234')
    alice.save()

    bob = factories.BobSomUserFactory.create()
    bob.set_password('1234')
    bob.save()


@pytest.fixture(scope='function')
def members_db(members):
    with connections['users_db'].cursor() as cursor:
        cursor.execute(
            '''CREATE TABLE som_users (
                 lang         varchar(10),
                 www_phone    varchar(64),
                 www_mobile   varchar(64),
                 www_soci     integer,
                 id           integer,
                 last_login   timestamp,
                 username     varchar(150),
                 first_name   varchar(30),
                 last_name    varchar(30),
                 email        varchar(254),
                 password     varchar(128),
                 is_active    boolean,
                 is_superuser boolean,
                 is_staff     boolean,
                 date_joined  timestamp
            );
            '''
        )
        for user in get_user_model().objects.all():
            cursor.execute(
                f'''INSERT INTO som_users values (
                    '{user.lang}',
                    '{user.www_phone}',
                    '{user.www_mobile}',
                    '{user.www_soci}',
                    '{user.id}',
                    '{user.last_login}',
                    '{user.username.upper()}',
                    '{user.first_name}',
                    '{user.last_name}',
                    '{user.email}',
                    '{user.password}',
                    '{user.is_active}',
                    '{user.is_superuser}',
                    '{user.is_staff}',
                    '{user.date_joined}'
                );
            '''
            )
    yield

    with connections['users_db'].cursor() as cursor:
        cursor.execute('DROP TABLE IF EXISTS som_users')


@pytest.fixture(scope='function')
def not_register_member():
    return factories.AliceSomUserFactory.create()


@pytest.fixture(scope='function')
def not_register_madrid_member(mock_madrid_address_codes):
    return factories.AliceSomUserFactory.create()


@pytest.fixture(scope='function')
def member_active_agregistry():
    return factories.ActiveAgRegistrationFactory.create()


@pytest.fixture(scope='function')
def member_inactive_agregistry():
    return factories.InactiveAgRegistrationFactory.create()


@pytest.fixture(scope='function')
def inperson_member_agregistry():
    return factories.ActiveAgRegistrationInPersonFactory.create()


@pytest.fixture(scope='function')
def pending_email_member_registry():
    return factories.PendingEmailAgRegistrationFactory.create()


@pytest.fixture(scope='function')
def pending_email_member_registry_localgroup_assembly():
    return factories.PendingEmailLocalGroupRegistrationFactory.create()
