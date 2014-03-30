# -*- coding: utf8 -*-
from account.views import AuthVk
from account.views import AuthSecureLink
from account.views import Summary
from account.views import Logout
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^auth/vk/$', AuthVk.as_view(), name='auth_vk'),
    url(r'^auth/secure_link/$', AuthSecureLink.as_view(), name='auth_secure_link'),
    url(r'^summary/$', Summary.as_view(), name='account_summary'),
    url(r'^auth/logout/$', Logout.as_view(), name='auth_logout')
)
