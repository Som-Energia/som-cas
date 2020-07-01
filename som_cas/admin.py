from django.contrib import admin
from django.utils.translation import gettext as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import SomUser, AgRegistration, Assembly


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


@admin.register(Assembly)
class AssemblyAdmin(admin.ModelAdmin):
    inlines = (MemberInline, )


class AgRegistrationResource(resources.ModelResource):

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
        import_id_fields = ('registration_date',)


@admin.register(AgRegistration)
class AgRegistrationAdmin(ImportExportModelAdmin):
    resource_class = AgRegistrationResource
