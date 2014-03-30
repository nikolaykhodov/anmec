# -*- coding: utf8 -*-

from StringIO import StringIO
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from account.models import Account
from account.models import Login
import mox
import json
import urllib2


class VkAuthFailCase(TestCase):

    def setUp(self):

        self.url_regexp = r'^https://oauth\.vk\.com/access_token\?client_secret=[^&]+&code=[^&]+&client_id=\d+&redirect_uri='

        self.client = Client()

        self.mox = mox.Mox()
        self.mox.StubOutWithMock(urllib2, 'urlopen')
        urllib2.urlopen(mox.Regex(self.url_regexp)).AndReturn(StringIO('{}'))
        self.mox.ReplayAll()

    def test_auth_fail(self):

        response = self.client.get(reverse('auth_vk'), {})

        self.assertEqual(response.status_code, 302)

        location = response._headers['location'][1]
        self.assertGreater(location.find('failed=true'), -1)

        response = self.client.get(reverse('auth_secure_link'), {})
        self.assertEqual(response.status_code, 200)

        secure_link = json.dumps(response.content)
        self.assertFalse('hash' in secure_link)
        self.assertFalse('expires_at' in secure_link)

    def tearDown(self):
        self.mox.UnsetStubs()


class VkAuthSuccessCase(TestCase):

    def setUp(self):

        self.url_regexp = r'^https://oauth\.vk\.com/access_token\?client_secret=[^&]+&code=[^&]+&client_id=\d+&redirect_uri='
        self.account = Account.objects.create_user(uid=1, network='vk')
        self.auth_success_mock = json.dumps(dict(access_token='1', user_id=1))

        self.client = Client()

        self.mox = mox.Mox()
        self.mox.StubOutWithMock(urllib2, 'urlopen')
        urllib2.urlopen(mox.Regex(self.url_regexp)).AndReturn(StringIO(self.auth_success_mock))
        self.mox.ReplayAll()

    def test_auth_success(self):

        response = self.client.get(reverse('auth_vk'), {}, **dict(
            HTTP_USER_AGENT='silly-human',
            REMOTE_ADDR='127.0.0.1'
        ))

        self.assertEqual(response.status_code, 302)

        location = response._headers['location'][1]
        self.assertGreater(location.find('authTransition.html'), -1)
        self.assertEqual(Login.objects.filter(account=self.account).count(), 1)

        response = self.client.get(reverse('auth_secure_link'), {})
        self.assertEqual(response.status_code, 200)

        secure_link = json.dumps(response.content)
        self.assertTrue('hash' in secure_link)
        self.assertTrue('expires_at' in secure_link)

    def tearDown(self):
        self.mox.UnsetStubs()


class VkAuthCreateAccountOnTheFlyCase(TestCase):

    def setUp(self):

        self.url_regexp = r'^https://oauth\.vk\.com/access_token\?client_secret=[^&]+&code=[^&]+&client_id=\d+&redirect_uri='
        self.auth_success_mock = json.dumps(dict(access_token='1', user_id=2))
        Account.objects.create_user(network='vk', uid=2)

        self.client = Client()

        self.mox = mox.Mox()
        self.mox.StubOutWithMock(urllib2, 'urlopen')
        urllib2.urlopen(mox.Regex(self.url_regexp)).AndReturn(StringIO(self.auth_success_mock))
        self.mox.ReplayAll()

    def test_auth_success(self):

        response = self.client.get(reverse('auth_vk'), {}, **dict(
            HTTP_USER_AGENT='silly-human',
            REMOTE_ADDR='127.0.0.1'
        ))

        self.assertEqual(response.status_code, 302)

        self.account = Account.objects.get(network='vk', uid=2)
        self.assertEqual(self.account.uid, 2)

        location = response._headers['location'][1]
        self.assertGreater(location.find('authTransition.html'), -1)
        self.assertEqual(Login.objects.filter(account=self.account).count(), 1)

        response = self.client.get(reverse('auth_secure_link'), {})
        self.assertEqual(response.status_code, 200)

        secure_link = json.dumps(response.content)
        self.assertTrue('hash' in secure_link)
        self.assertTrue('expires_at' in secure_link)

    def tearDown(self):
        self.mox.UnsetStubs()


class AccountSummaryCase(TestCase):

    def setUp(self):

        self.client = Client()

    def test_unauthenticated_user(self):

        response = self.client.get(reverse('account_summary'))

        self.assertEqual(response.status_code, 200)
        summary = json.loads(response.content)
        self.assertEqual(summary, {'loggedIn': False})
