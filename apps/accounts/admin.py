from django.contrib import admin

from . import models

class AccountAdmin(admin.ModelAdmin):
    list_display = ('number',)

admin.site.register(models.Account, AccountAdmin)