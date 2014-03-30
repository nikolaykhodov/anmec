# -*- coding: utf-8 -*-

from django.test import TestCase
from anmec_utils.helpers import camel_case_dict

class CamelCaseDictCase(TestCase):

    def test_1(self):
        source = {'t_t': 1, 'repost_like_ratio': 80}
        end = camel_case_dict(source)

        self.assertEqual(end, {'tT': 1, 'repostLikeRatio': 80})
