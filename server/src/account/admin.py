# -*- coding: utf8 -*-

from django.contrib import admin
from account.models import Login
from account.models import Account


class LoginAdmin(admin.ModelAdmin):
    list_display = ('profile_link', 'timestamp', 'ip', 'ua')
    search_fields = ['account__uid', 'account__network', 'ip', 'ua']


class AccountAdmin(admin.ModelAdmin):
    list_display = ('profile_link', 'uid', 'network', 'paid_till')
    search_fields = ['uid', 'network', 'paid_till']


admin.site.register(Account, AccountAdmin)
admin.site.register(Login, LoginAdmin)
