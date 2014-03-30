# -*- coding: utf8 -*-

"""
Авторизация пользователя и ограничение доступа
"""

from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from anmec_utils.decorators import json_answer
from account.helpers import auth_user
from account.helpers import get_secure_link_hash
from urllib import urlencode


import urllib2
import json

import time


class AuthVk(View):

    def _auth(self):
        if settings.DEBUG is True and self.request.GET.get('code', '') == 'debug':
            return auth_user(self.request, 156261930, 'vk', '')

        # URL для валидации кода
        uri = 'https://oauth.vk.com/access_token?' + urlencode(dict(
            client_id=settings.VK_APP_ID,
            client_secret=settings.VK_APP_KEY,
            code=self.request.GET.get('code'),
            redirect_uri='http://%s%s' % ('app.anmec.me' if not settings.DEBUG else 'app-debug.anmec.me:8000', reverse('auth_vk'))
        ))
        try:
            answer = json.loads(urllib2.urlopen(uri).read())
            access_token = answer['access_token']
            user_id = int(answer['user_id'])
        except (urllib2.HTTPError, KeyError, ValueError):
            return False

        return auth_user(self.request, user_id, 'vk', access_token)

    def calculate_secure_link(self):

        expires_at = int(time.time()) + 24 * 3600
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')

        return dict(
            expires_at=expires_at,
            hash=get_secure_link_hash(settings.SECURE_LINK_SECRET, user_agent, expires_at)
        )

    def get(self, request):

        if settings.DEBUG is False:
            redirect_url = 'http://ver2.anmec.me/'
        else:
            redirect_url = 'http://www-debug.anmec.me/'

        if self._auth() is True:
            secure_link = self.calculate_secure_link()
            self.request.session['secure_link'] = secure_link
            redirect_url += "authTransition.html"
        else:
            redirect_url += '#/login?failed=true'

        return HttpResponseRedirect(redirect_url)


class Logout(View):

    @json_answer
    def get(self, request):
        logout(request)
        return {}


class AuthSecureLink(View):

    @json_answer
    def get(self, request):

        if request.user.is_authenticated():
            return request.session['secure_link']
        else:
            return {}


class Summary(View):

    @json_answer
    def get(self, request):

        if not request.user.is_authenticated():
            return dict(
                loggedIn=False
            )
        else:
            account = request.session['account']
            return dict(
                loggedIn=True,
                userName=account.network + '_' + str(account.uid),
                vk_token=str(account.vk_token)
            )
