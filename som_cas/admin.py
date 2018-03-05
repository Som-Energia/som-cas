from django.contrib import admin

from .models import SomUser

# Register your models here.
@admin.register(SomUser)
class SomUserAdmin(admin.ModelAdmin):
    pass
