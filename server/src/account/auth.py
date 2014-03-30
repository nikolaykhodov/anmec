# -*- coding: utf8 -*-

from account.models import Account


class AccountBackend:
    """
    Авторизация через социальный аккаунт
    """

    def authenticate(self, uid=None, network=None):
        """
        Авторизуем
        """

        try:
            account = Account.objects.get(uid=uid, network=network)
        except Account.DoesNotExist:
            account = Account.objects.create_user(uid=uid, network=network)

        return account

    def get_user(self, username):
        try:
            return Account.objects.get(pk=username)
        except Account.DoesNotExist:
            return None
