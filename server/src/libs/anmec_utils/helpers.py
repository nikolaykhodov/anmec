# -*- coding: utf-8 -*-

from django.conf import settings
import re


def prepare_sphinx_query(query):
    parts = re.split(r'[!.?,;:"-\\ ]', query)
    parts = [part[:4] + '*' for part in parts if len(part) >= settings.SPHINX_MIN_LENGTH]
    return " & ".join(parts)


def str2int(s):
    """ Return integer, otherwise None """

    retVal = None
    try:
        retVal = int(s)
    except (ValueError, TypeError):
        pass

    return retVal


def get_all_form_errors(form):
    """
    Возвращает список всех ошибок в форме в одном массиве

    Параметры:
        -- form - форма
    """

    # Объединить все ошибки в один массив
    errors = []
    for field in form.errors.keys():
        for error in form.errors[field]:
            if field == '__all__':
                field_name = ''
            else:
                if form.fields[field].label:
                    field_name = form.fields[field].label
                else:
                    field_name = field

                field_name = field_name + ': '

            errors.append(
                '%s%s' % (field_name, error)
            )

    return errors


def camel_case_dict(dictionary):

    retVal = {}

    for old_key in dictionary.keys():
        # group_name --> groupName
        matches = re.findall(r'([a-z])_([a-z])', old_key)

        new_key = old_key
        for match in matches:
            old_couple = match[0] + '_' + match[1]
            new_couple = match[0] + match[1].upper()
            new_key = new_key.replace(old_couple, new_couple, 1)

        retVal[new_key] = dictionary[old_key]

    return retVal
