# -*- coding: utf8 -*-

from jsonforms.forms import JSONForm
from django import forms


class SearchGroupsForm(JSONForm):

    group_name__value = forms.CharField(required=False)

    quantity__from = forms.IntegerField(required=False)
    quantity__to = forms.IntegerField(required=False)

    group_privacy__public = forms.BooleanField(required=False)
    group_privacy__closed = forms.BooleanField(required=False)
    group_privacy__private = forms.BooleanField(required=False)

    group_type__group = forms.BooleanField(required=False)
    group_type__event = forms.BooleanField(required=False)
    group_type__public = forms.BooleanField(required=False)

    visitors__from = forms.IntegerField(required=False)
    visitors__to = forms.IntegerField(required=False)

    views__from = forms.IntegerField(required=False)
    views__to = forms.IntegerField(required=False)

    reach__from = forms.IntegerField(required=False)
    reach__to = forms.IntegerField(required=False)

    sex__female = forms.IntegerField(required=False)
    sex__male = forms.IntegerField(required=False)

    over18__from = forms.IntegerField(required=False)
    over18__to = forms.IntegerField(required=False)

    region__country = forms.IntegerField(required=False)
    region__city = forms.IntegerField(required=False)
    region__from = forms.IntegerField(required=False)

    order_by = forms.CharField(required=False)
    offset = forms.IntegerField(required=False)


class SearchPostsForm(JSONForm):

    keyword__value = forms.CharField(required=False)
    time_frame__from = forms.IntegerField(required=False)
    likes__from = forms.IntegerField(required=False)
    reposts__from = forms.IntegerField(required=False)
    repost_like_ratio__from = forms.IntegerField(required=False)
    attachment_filter = forms.CharField(required=False)

    order_by = forms.CharField(required=False)
    page = forms.IntegerField(required=False)
