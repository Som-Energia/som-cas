import tablib
import yaml
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from .models import SomUser, AgRegistration, Assembly, LocalGroups

class MemberInline(admin.TabularInline):
    model = AgRegistration
    fields = ('member', 'registration_email_sent', 'registration_type', )
    raw_id_fields = ('member',)
    readonly_fields = ('member',)
    show_change_link = True
    can_delete = False
    extra = 0


@admin.register(SomUser)
class SomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('email', 'password', )
        }),
        ("Personal info", {
            'fields': ('username', 'lang', 'www_soci', )
        }),
        ("Permissions", {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'user_permissions', )
        }),
        ("Important dates", {
            'fields': ('last_login', )
        })
    )

    def member_number(self, obj):
        return obj.www_soci

    member_number.short_description = _('member')

    list_display = ('username', 'member_number', 'email', )
    search_fields = ('username', 'email', )


    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(www_soci=search_term_as_int)
        return queryset, use_distinct


@admin.register(Assembly)
class AssemblyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date',
        'active'
    )
    list_filter = (
        'name',
        'date'
    )

    inlines = (MemberInline, )


class AgRegistrationResource(resources.ModelResource):
    assembly = resources.Field(
        attribute='assembly__name',
        column_name=_('Assembly')
    )

    registration_date = resources.Field(
        attribute='date',
        column_name=_('Registration date')
    )

    member_fullname = resources.Field(
        attribute='member__full_name',
        column_name=_('Member name')
    )

    member_number = resources.Field(
        attribute='member__www_soci',
        column_name=_('Membership number')
    )

    member_vat = resources.Field(
        attribute='member__username',
        column_name=_('DNI/NIF/NIE')
    )

    member_email = resources.Field(
        attribute='member__email',
        column_name=_('Email')
    )

    class Meta:
        model = AgRegistration
        fields = (
            'member_name', 'member_number', 'member_vat', 'registration_date',
            'member_email'
        )
        import_id_fields = ('registration_date', 'member_vat',)



@admin.register(AgRegistration)
class AgRegistrationAdmin(ImportExportModelAdmin):

    def assembly_name(self, obj):
        return obj.assembly.name

    def member_vat(self, obj):
        return obj.member.username

    list_display = (
        'assembly_name',
        'member_vat',
        'date',
        'registration_type',
        'registration_email_sent'
    )
    list_filter = (
        'assembly__name',
    )
    resource_class = AgRegistrationResource
    search_fields = ('assembly__name', 'member__username',)
    autocomplete_fields = ('member',)


class LocalGroupsResource(resources.ModelResource):
    name = resources.Field(
        attribute='name'
    )

    data = resources.Field(
        attribute='data',
    )

    full_name = resources.Field(
        attribute='full_name'
    )

    alias = resources.Field(
        attribute='alias'
    )

    email = resources.Field(
        attribute='email'
    )

    logo = resources.Field(
        attribute='logo'
    )

    class Meta:
        model = LocalGroups
        fields = ('name', 'data', 'full_name', 'alias', 'email', 'logo')
        import_id_fields = ('name',)

    def import_data(self, dataset, dry_run=False, raise_errors=False, use_transactions=None, collect_failed_rows=False, **kwargs):
        new_data = [{'name': header, 'data': dataset[header][0]}
            for header in dataset.headers
        ]
        new_dataset = tablib.Dataset()
        new_dataset.dict = new_data

        return super().import_data(new_dataset, dry_run=dry_run, raise_errors=raise_errors, use_transactions=use_transactions, collect_failed_rows=collect_failed_rows, **kwargs)


def _create_dataset(cls, in_stream, **kwargs):
    data = yaml.safe_load(in_stream)
    dataset = tablib.Dataset()
    dataset.dict = data if isinstance(data, list) else [data]
    return dataset


@admin.register(LocalGroups)
class LocalGroupsAdmin(ImportExportModelAdmin):
    list_display = (
        'name',
        'email'
    )

    resource_class = LocalGroupsResource

    def get_import_formats(self):
        yaml_format = base_formats.YAML
        yaml_format.create_dataset = _create_dataset
        return [yaml_format]
