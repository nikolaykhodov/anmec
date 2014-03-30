# -*- coding: utf8 -*-

from django import forms
import json
import re


class JSONForm(forms.Form):

    def _flatten_dict(self, dictionary, prefix=''):
        """ Flatten a dictionary in camel-cased notation """

        flat_dict = {}

        for key in dictionary.keys():
            # groupName --> group_name
            flat_key = re.sub(r'([a-z])([A-Z])', '\\1_\\2', key).lower()

            value = dictionary[key]
            if isinstance(value, dict) is True:
                flat_dict.update(
                    self._flatten_dict(value, prefix + flat_key + '__')
                )
            else:
                flat_dict[prefix + flat_key] = value

        return flat_dict

    def clean(self, *args, **kwargs):
        if self.json_decoding_error is True:
            raise forms.ValidationError, "No JSON object could be decoded"

        return super(JSONForm, self).clean(*args, **kwargs)

    def __init__(self, data=None, **kwargs):
        self.json_decoding_error = False
        parsed_data = data

        if data is not None:
            try:
                parsed_data = json.loads(data)
                parsed_data = self._flatten_dict(parsed_data)
            except ValueError:
                self.json_decoding_error = True
                parsed_data = None

        super(JSONForm, self).__init__(data=parsed_data, **kwargs)
