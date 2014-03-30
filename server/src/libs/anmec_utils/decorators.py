# -*- coding: utf8 -*-

from django.http import HttpResponse
import json


def json_answer(func):
    """ Декоратор для возврата HttpResponse по JSON-ответу """

    def wrapper(*args, **kwargs):
        return HttpResponse(json.dumps(func(*args, **kwargs)))

    return wrapper
