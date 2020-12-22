from datetime import datetime, timedelta

import factory
from django.utils import timezone as tz
from som_cas.models import (AgRegistration, Assembly, LocalGroups,
                            RegistrationChoices, SomUser)
from . import personaldata


class LocalGroupsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = LocalGroups


class BaixMontsenyFactory(LocalGroupsFactory):

    name = 'BaixMontseny'

    data = {
        'name': 'Baix Montseny',
        'alias': {
            'city': [
                '17009', '17027', '08039', '08042', '08046', '08097', '08097', '17083', '08106', '17101', '08137', '17146', '08198', '08202', '08207', '17159', '17164', '08234', '08259', '08294', '08306'
            ]
        }
    }


class AlmeriaFactory(LocalGroupsFactory):

    name = 'Almeria'

    data = {
        'name': 'Almería',
        'alias': {
            'state': ['04']
        }
    }


class CMadridFactory(LocalGroupsFactory):

    name = 'Comunidad de Madrid'

    data = {
        'name': 'Comunidad de Madrid',
        'alias': {
            'ccaa': ['13']
        }
    }


class AssemblyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Assembly

    date = factory.Faker(
        'date_between_dates',
        date_start=datetime(2020, 1, 1, tzinfo=tz.get_current_timezone())
    )

    start_votation_date = factory.Faker(
        'date_between_dates',
        date_start=datetime(2020, 1, 1, 12, 5, tzinfo=tz.get_current_timezone())
    )

    end_votation_date = factory.Faker(
        'date_between_dates',
        date_start=factory.SelfAttribute('..start_votation_date')
    )


class ActiveGeneralAssemblyFactory(AssemblyFactory):

    name = 'General Assambly'
    active = True


class InactiveGeneralAssemblyFactory(AssemblyFactory):

    name = 'General Assambly'
    active = False


class ActiveMadridLocalGroupAssemblyFactory(AssemblyFactory):

    name = 'Madrid Local Group Assembly'
    active = True
    local_group = factory.SubFactory(CMadridFactory)


class ActiveBaixMontsenyLocalGroupAssemblyFactory(AssemblyFactory):

    name = 'Baix Montseny Local Group Assembly'
    active = True
    local_group = factory.SubFactory(BaixMontsenyFactory)


class SomUserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = SomUser

    date_joined = datetime.now()
    last_login = datetime.now()


class AliceSomUserFactory(SomUserFactory):
    '''
    Alice acts as a non yet assembly register member
    '''
    class Meta:
        model = SomUser
        django_get_or_create = ('username',)

    username = 'Alice'
    first_name = 'Alice'
    www_soci = 666
    email = personaldata.email


class BobSomUserFactory(SomUserFactory):
    '''
    Bob acts as already virtual assembly register member
    '''
    username = 'Bob'
    www_soci = 999


class MikaSomUserFactory(SomUserFactory):
    '''
    Mika acts as already in person assembly register member
    '''
    username = 'Mika'
    www_soci = 16


class AgRegistrationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = AgRegistration

    date = factory.LazyFunction(datetime.now)
    registration_type = RegistrationChoices.VIRTUAL


class ActiveAgRegistrationFactory(AgRegistrationFactory):

    member = factory.SubFactory(BobSomUserFactory)
    assembly = factory.SubFactory(ActiveGeneralAssemblyFactory)
    registration_email_sent = True


class PendingEmailAgRegistrationFactory(AgRegistrationFactory):

    member = factory.SubFactory(AliceSomUserFactory)
    assembly = factory.SubFactory(ActiveGeneralAssemblyFactory)
    registration_email_sent = False

class SomUserActiveRegistryFactory(BobSomUserFactory):

    registered = factory.RelatedFactory(
        ActiveAgRegistrationFactory,
        factory_related_name='member'
    )


class InactiveAgRegistrationFactory(AgRegistrationFactory):

    assembly = factory.SubFactory(InactiveGeneralAssemblyFactory)


class OldAgRegistrationFactory(AgRegistrationFactory):

    member = factory.SubFactory(AliceSomUserFactory)
    assembly = factory.SubFactory(InactiveGeneralAssemblyFactory)


class SomUserInactiveRegistryFactory(AliceSomUserFactory):

    registered = factory.RelatedFactory(
        InactiveAgRegistrationFactory,
        factory_related_name='member'
    )


class ActiveAgRegistrationInPersonFactory(AgRegistrationFactory):

    assembly = factory.SubFactory(ActiveGeneralAssemblyFactory)
    registration_type = RegistrationChoices.INPERSON


class SomUserActiveRegistryInPersonFactory(MikaSomUserFactory):

    registered = factory.RelatedFactory(
        ActiveAgRegistrationInPersonFactory,
        factory_related_name='member'
    )
