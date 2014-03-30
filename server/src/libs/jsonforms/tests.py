# -*- coding: utf8 -*-

from django.test import TestCase
from jsonforms.forms import JSONForm
from django import forms
import json

TEST_DATA = dict(
    groupName=dict(
        value='ABCD'
    ),

    quantity={
        'from': 0,
        'to': 123
    }
)


class TestForm(JSONForm):

    group_name__value = forms.CharField()
    quantity__from = forms.IntegerField()
    quantity__to = forms.IntegerField()


class JsonFormTest(TestCase):

    def test_basic(self):
        """ """

        post_data = json.dumps(TEST_DATA)
        form = TestForm(data=post_data)

        if not form.is_valid():
            print form._errors

        self.assertEqual(form.is_valid(), True)

        d = form.cleaned_data
        self.assertEqual(d['group_name__value'], 'ABCD')
        self.assertEqual(d['quantity__from'], 0)
        self.assertEqual(d['quantity__to'], 123)

    def test_erroneous_body(self):

        form = TestForm(data=']')

        self.assertEqual(form.is_valid(), False)
