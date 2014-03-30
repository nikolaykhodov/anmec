# -*- coding: utf8 -*-

from search.models import Post
from search.models import Group
from search.models import Audience
from search.models import TrafficByCities
from search.models import TrafficByCountries

from anmec_utils.decorators import json_answer
from anmec_utils.helpers import str2int
from anmec_utils.helpers import prepare_sphinx_query
from anmec_utils.helpers import get_all_form_errors
from anmec_utils.helpers import camel_case_dict

from search.forms import SearchGroupsForm
from search.forms import SearchPostsForm

from search.sphinx import search_for

from django.core.cache import cache
from django.views.generic.base import View
from django.db.models import Q
from django.conf import settings

from datetime import datetime
from datetime import timedelta

import urllib2
import re
import time


class Index(View):

    @json_answer
    def get(self, request):
        return {}


class FindGroups(View):

    def apply_basic_filters(self, queryset, data):

        name = data.get('group_name__value')
        if name is not None:
            query = prepare_sphinx_query(name)
            if query != '':
                ids = cache.get('sphinx_results_for_' + name)
                if ids is None:
                    ids = search_for(query, settings.SPHINX_GROUPS_INDEX)
                    cache.set('sphinx_results_for_' + name, ids)
                queryset = queryset.filter(gid__in=ids)

        members_from = data.get('quantity__from')
        if members_from is not None:
            queryset = queryset.filter(members_count__gte=members_from)

        members_to = data.get('quantity_to')
        if members_to is not None:
            queryset = queryset.filter(members_count__lte=members_to)

        prefix = 'group_privacy__'
        privacy_types = {'public': 0, 'closed': 1, 'private': 2}
        privacy_condition = Q()
        for privacy in privacy_types:
            if data.get(prefix + privacy) is True:
                privacy_condition = privacy_condition | Q(is_closed=privacy_types[privacy])
        queryset = queryset.filter(privacy_condition)

        prefix = 'group_type__'
        group_types = {'group': 1, 'event': 2, 'public': 3}
        group_type_condition = Q()
        for gt in group_types:
            if data.get(prefix + gt) is True:
                group_type_condition = group_type_condition | Q(type=group_types[gt])
        queryset = queryset.filter(group_type_condition)

        return queryset

    def apply_audience_filters(self, queryset, data):

        # Visitors
        visitors_from = data.get('visitors__from')
        visitors_to = data.get('visitors__to')

        if visitors_from is not None:
            queryset = queryset.filter(audience__visitors__gte=visitors_from)

        if visitors_to is not None:
            queryset = queryset.filter(audience__visitors__lte=visitors_to)

        # Views
        views_from = data.get('views__from')
        views_to = data.get('views__to')

        if views_from is not None:
            queryset = queryset.filter(audience__views__gte=views_from)

        if views_to is not None:
            queryset = queryset.filter(audience__views__lte=views_to)

        # Reach
        reach_from = data.get('reach__from')
        reach_to = data.get('reach__to')

        if reach_from is not None:
            queryset = queryset.filter(audience__reach__gte=reach_from)

        if reach_to is not None:
            queryset = queryset.filter(audience__reach__lte=reach_to)

        # Sex
        sex_female_from = data.get('sex__female')
        sex_male_from = data.get('sex__male')

        if sex_female_from is not None:
            queryset = queryset.filter(audience__female__gte=sex_female_from)

        if sex_male_from is not None:
            queryset = queryset.filter(audience__male__gte=sex_male_from)

        # 18+
        over18_from = data.get('over18__from')
        over18_to = data.get('over18__to')

        if over18_from is not None:
            queryset = queryset.filter(audience__over18__gte=over18_from)

        if over18_to is not None:
            queryset = queryset.filter(audience__over18__lte=over18_to)

        return queryset

    def apply_region_filters(self, queryset, data):
        country = data.get('region__country')
        city = data.get('region_city')
        fraction = data.get('region_from')

        if fraction is None:
            return queryset

        if city is not None and city > -1:
            ids_queryset = TrafficByCities.objects.filter(cid=city).filter(visitors__gte=fraction).values_list('group_id')
            queryset = queryset.filter(gid__in=ids_queryset)
        elif country is not None:
            ids_queryset = TrafficByCountries.objects.filter(cid=country).filter(visitors__gte=fraction).values_list('group_id')
            queryset = queryset.filter(gid__in=ids_queryset)

        return queryset

    def get_city_traffic(self, gids, data):
        city = data.get('region__city')

        info = list(
            TrafficByCities.objects.filter(group_id__in=gids).filter(cid=city).values('visitors', 'group_id')
        )

        traffic = {}
        for entry in info:
            traffic[entry['group_id']] = entry['visitors']

        return traffic

    def get_country_traffic(self, gids, data):
        country = data.get('region__country')

        if country is None:
            return {}

        info = list(
            TrafficByCountries.objects.filter(group__in=gids).filter(cid=country).values('visitors', 'group_id')
        )

        print info

        traffic = {}
        for entry in info:
            traffic[entry['group_id']] = entry['visitors']

        return traffic

    def get_order_by_column(self, data):
        return data.get('order_by') or '-members_count'

    def get_offset(self, data):
        try:
            offset = int(data.get('offset', 0))
            if offset < 0:
                offset = 0
        except (ValueError, TypeError):
            offset = 0

        return offset

    def get_related_field_names(self, model, model_prefix=True):
        prefix = model._meta.module_name + '__' if model_prefix is True else ''
        return [prefix + field.name for field in model._meta.fields]

    @json_answer
    def post(self, request):

        form = SearchGroupsForm(data=request.body)

        if form.is_valid() is False:
            return dict(errors=get_all_form_errors(form))

        data = form.cleaned_data

        results_per_page = settings.RESULTS_PER_PAGE
        offset = self.get_offset(data)
        column = self.get_order_by_column(data)

        gids_queryset = Group.objects
        gids_queryset = self.apply_basic_filters(gids_queryset, data)
        gids_queryset = self.apply_audience_filters(gids_queryset, data)
        gids_queryset = self.apply_region_filters(gids_queryset, data)
        gids_queryset = gids_queryset.order_by(column)
        gids_queryset = gids_queryset.distinct()
        gids_queryset = gids_queryset.values_list('gid', flat=True)
        gids = list(gids_queryset[offset:offset + results_per_page])

        fields = self.get_related_field_names(Group, False)
        fields.extend(self.get_related_field_names(Audience))
        groups = list(
            Group.objects.filter(gid__in=gids).select_related('audience').order_by(column).values(*fields)
        )

        city_traffic = self.get_city_traffic(gids, data)
        country_traffic = self.get_country_traffic(gids, data)
        for group in groups:
            group['country_traffic'] = country_traffic.get(group['gid'])
            group['city_traffic'] = city_traffic.get(group['gid'])

        return dict(
            groups=groups,
            count=len(groups)
        )


class FindPosts(View):

    def get_order_by_column(self, data):
        return data.get('order_by') or '-likes'

    def get_page(self, data):

        page = str2int(data.get('page')) or 1
        if page < 1:
            page = 1

        return page

    def apply_keyword_filter(self, queryset, data):

        keyword = data.get('keyword__value')

        if keyword is not None:
            query = prepare_sphinx_query(keyword)
            if query != '':
                ids = cache.get('sphinx_results_for_' + keyword)
                if ids is None:
                    ids = search_for(query, settings.SPHINX_POSTS_INDEX)
                    cache.set('sphinx_results_for_' + keyword, ids)
                queryset = queryset.filter(id__in=ids)

        return queryset

    def apply_like_filters(self, queryset, data):

        likes_from = data.get('likes__from')
        if likes_from is not None:
            queryset = queryset.filter(likes__gte=likes_from)

        reposts_from = data.get('reposts__from')
        if reposts_from is not None:
            queryset = queryset.filter(reposts__gte=reposts_from)

        repost_like_ratio_from = data.get('repost_like_ratio__from')
        if repost_like_ratio_from is not None:
            queryset = queryset.filter(repost_like_ratio__gte=repost_like_ratio_from)

        time_frame_from = data.get('time_frame__from')
        if time_frame_from is not None:
            queryset = queryset.filter(date__gte=datetime.now() + timedelta(days=-time_frame_from))

        return queryset

    def format_posts(self, posts):
        new_posts = []

        for post in posts:
            post['date'] = int(time.mktime(post['date'].timetuple()))
            #post['attachments'] = ''

            new_posts.append(camel_case_dict(post))

        return new_posts

    def get_offset(self, data):
        try:
            offset = int(data.get('offset', 0))

            if offset < 0:
                offset = 0
        except (TypeError, ValueError):
            offset = 0

        return offset

    @json_answer
    def post(self, request):
        form = SearchPostsForm(data=request.body or '{}')

        if form.is_valid() is False:
            return dict(errors=get_all_form_errors(form))

        data = form.cleaned_data

        results_per_page = settings.RESULTS_PER_PAGE
        page = self.get_page(data)
        column = self.get_order_by_column(data)

        posts_queryset = Post.objects
        posts_queryset = self.apply_keyword_filter(posts_queryset, data)
        posts_queryset = self.apply_like_filters(posts_queryset, data)
        posts_queryset = posts_queryset.order_by(column)

        #posts_queryset = posts_queryset.distinct()

        offset = self.get_offset(data)
        posts_queryset = posts_queryset.values()
        posts = list(posts_queryset[offset:offset + results_per_page])
        posts = self.format_posts(posts)

        count = posts_queryset.count()
        max_page = (count / results_per_page) + 1
        return dict(
            posts=posts,
            page=page,
            count=posts_queryset.count(),
            maxPage=max_page
        )

    get = post


class Proxy(View):

    @json_answer
    def data(self, request):

        retVal = {}
        for key in request.POST.keys():
            url = request.POST[key]
            response = ''

            if len(re.findall(r'^https?://vk.com/', url)) > 0:
                response = urllib2.urlopen(url, None, 3).read().decode('cp1251')

            retVal[key] = response

        return retVal
