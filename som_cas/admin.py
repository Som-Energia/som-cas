from django.contrib import admin

from .models import SomUser, AgRegistration


# Register your models here.
@admin.register(SomUser)
class SomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(AgRegistration)
class AgRegistrationAdmin(admin.ModelAdmin):
    pass
