from django.contrib import admin

from .models import SomUser, AgRegistration, Assambley


class MemberInline(admin.TabularInline):
    model = Assambley.registered.through
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


@admin.register(Assambley)
class AssambleyAdmin(admin.ModelAdmin):
    inlines = (MemberInline, )


@admin.register(AgRegistration)
class AgRegistrationAdmin(admin.ModelAdmin):
    pass
