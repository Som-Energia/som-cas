import pytest
from erppeek import Client

from som_cas.middleware import _set_erp_connection
from . import factories


@pytest.fixture
def erp_con(settings):
    return _set_erp_connection(lambda self: Client(**settings.ERP))


@pytest.fixture(autouse=True)
def set_debug_when_testing(settings):
    settings.DEBUG = True


@pytest.fixture
def local_group():
    factories.BaixMontsenyFactory.create()
    factories.AlmeriaFactory.create()
    factories.CMadridFactory.create()


@pytest.fixture
def assemblies():
    factories.ActiveGeneralAssamblyFactory.create()
    factories.InactiveGenerealAssamblyFactory.create()
    factories.ActiveLocalGroupAssemblyFactory.create()
    factories.InactiveGeneralAssemblyFactory.create()


@pytest.fixture
def active_general_assembly():
    return factories.ActiveGeneralAssemblyFactory.create()


@pytest.fixture
def inactive_general_assembly():
    return factories.InactiveGeneralAssemblyFactory.create()


@pytest.fixture
def old_register_in_general_assembly():
    return factories.OldAgRegistrationFactory.create()


@pytest.fixture
def user():
    return factories.SomUserFactory.build()


@pytest.fixture
def members():
    factories.AliceSomUserFactory.create()
    factories.BobSomUserFactory.create()


@pytest.fixture
def not_register_member():
    return factories.AliceSomUserFactory.create()


@pytest.fixture
def member_registry():
    return factories.ActiveAgRegistrationFactory.create()


@pytest.fixture
def member_inactive_registry():
    return factories.InactiveAgRegistrationFactory.create()


@pytest.fixture
def inperson_member_registry():
    return factories.ActiveAgRegistrationInPersonFactory()
