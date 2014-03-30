# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from string import letters
from random import choice
from datetime import date
from account.managers import AccountManager


class Account(User):

    NETWORK_CHOICES = (
        ('vk', 'vk.com'),
        ('fb', 'facebook.com'),
        ('tw', 'twitter.com')
    )

    class Meta:
        unique_together = (('uid', 'network'),)

    uid = models.IntegerField(blank=False)
    network = models.CharField(max_length=2, blank=False, choices=NETWORK_CHOICES)
    paid_till = models.DateField(default='1970-01-01')
    vk_token = models.CharField(max_length=128, default='', db_index=True)

    objects = AccountManager()

    def refresh_token(self):
        """ Возвращает новый токен для пользователя """

        self.token = "".join([choice(letters) for i in xrange(64)])
        self.save()

        return self.token

    def __unicode__(self):
        return u'%s@%s' % (self.uid, self.network)

    def is_valid_subscription(self):
        if date.today() <= date(2013, 4, 21):
            return True
        else:
            return date.today() <= self.paid_till

    def profile_link(self):
        if self.network == 'vk':
            return u'<a href="https://vk.com/id%s" target="_blank">id%s</a>' % (self.uid, self.uid)
        else:
            return ''

    profile_link.allow_tags = True
    profile_link.short_description = 'Profile Link'


class Login(models.Model):

    account = models.ForeignKey(Account)
    timestamp = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=15, db_index=True)
    ua = models.TextField()

    def profile_link(self):
        return self.account.profile_link()

    profile_link.allow_tags = True
    profile_link.short_description = 'Profile Link'
