# -*- coding: utf8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from account.models import Account
import json


class FindGroupsCase(TestCase):

    def setUp(self):

        self.client = Client()
        self.account = Account.objects.create_user(uid=1, network='vk')
        self.client.login(uid=1, network='vk')

    def test_200(self):

        response = self.client.post(reverse('find_groups'), {})
        self.assertEqual(response.status_code, 200)

    def test_query(self):

        response = self.client.post(
            reverse('find_groups'),
            '{"page":1,"region":{"country":"1","city":"-1"},"quantity":{"from":"1000","to":"11000"},"visitors":{"to":"1000"},"views":{"to":"1000"},"reach":{"to":"10000"},"sex":{"male":"10","female":"10"},"over18":{"from":"10","to":"99"},"groupPrivacy":{"public":true},"groupType":{"group":true,"public":true}}',
            content_type='bla-bla'
        )
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.content)
        self.assertEqual(response['count'], 0)


class FindPostsCase(TestCase):

    def setUp(self):

        self.client = Client()
        self.account = Account.objects.create_user(uid=1, network='vk')
        self.client.login(uid=1, network='vk')

    def test_200(self):

        response = self.client.post(reverse('find_groups'), {})
        self.assertEqual(response.status_code, 200)

    def test_query(self):

        response = self.client.post(
            reverse('find_groups'),
            '{"page":1,"region":{"country":"1","city":"-1"},"quantity":{"from":"1000","to":"11000"},"visitors":{"to":"1000"},"views":{"to":"1000"},"reach":{"to":"10000"},"sex":{"male":"10","female":"10"},"over18":{"from":"10","to":"99"},"groupPrivacy":{"public":true},"groupType":{"group":true,"public":true}}',
            content_type='bla-bla'
        )
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.content)
        self.assertEqual(response['count'], 0)
