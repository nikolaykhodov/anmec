# -*- coding: utf8 -*-

"""
Вспомогательные функции
"""

from django.contrib.auth import authenticate
from django.contrib.auth import login
from account.models import Login
import hashlib
import base64


def auth_user(request, uid, network, access_token=''):
    """ Авторизует пользователя и возвращает HttpResponse """

    # Авторизуем пользователя
    account = authenticate(uid=uid, network=network)

    # Create an account on-the-fly
    if account is None:
        return False

    login(request, account)

    # Записываем историю входов
    Login.objects.create(account=account, ip=request.META['REMOTE_ADDR'], ua=request.META['HTTP_USER_AGENT'])

    account.vk_token = access_token
    account.save()

    request.session['account'] = account

    return True


def get_secure_link_hash(secret, user_agent, expires_at):

    hash = hashlib.md5(secret + user_agent + str(expires_at)).digest()
    hash = base64.b64encode(hash)
    hash = hash.replace('+', '-')
    hash = hash.replace('/', '_')
    hash = hash.replace('=', '')

    return hash
