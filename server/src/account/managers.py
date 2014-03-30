# -*- coding: utf8 -*-

from django.db import models
from django.contrib.auth.models import User


class AccountManager(models.Manager):

    def create_user(self, uid, network, *args, **kwargs):

        username = '{0}_{1}'.format(network, uid)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                *args, **kwargs
            )
        return self.create(user_ptr=user, username=username, uid=uid, network=network)
