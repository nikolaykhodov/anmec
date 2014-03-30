# -*- coding: utf-8 -*-

"""
Import group traffic analytics from JSON-parsed into DB
"""

from django.core.management.base import BaseCommand
from collections import namedtuple
from search import models
import json
import csv

Analytics = namedtuple('Analytic', ['audience', 'countries', 'cities', 'gid'])
Audience = namedtuple('Stat', ['reach', 'reach_subscribers', 'views', 'visitors', 'female', 'male', 'over18'])

class Command(BaseCommand):

    args = '<CSV with raw analytics data>'
    help = "Import analytics"


    def avg(self, map_func, array):

        mapped = map(map_func, array)

        if len(array) == 0:
            raise Exception, "Zero-length array"
        elif len(array) == 1:
            return mapped[0]
        else:
            S = reduce(lambda x, y: x+y, mapped)
            return S / len(array)

    def compute_female_visitors(self, data):
        """
        Compute the average number of female visitors in the course of interval covered by 'data'
        """

        S = 0

        # For each day
        for day in data:
            # Sex part
            sex = day.get('sex', [])

            # Leave only 'f'emale entry
            female_entry = filter(lambda y: y.get('value') == 'f', sex)
            if len(female_entry) == 0:
                continue

            # Add
            S += female_entry[0].get('visitors')

        return S / len(data)

    def compute_male_visitors(self, data):
        """
        Compute the average number of male visitors in the course of interval covered by 'data'
        """

        S = 0

        # For each day
        for day in data:
            # Sex part
            sex = day.get('sex', [])

            # Leave only 'm'ale entry
            male_entry = filter(lambda y: y.get('value') == 'm', sex)
            if len(male_entry) == 0:
                continue

            # Add
            S += male_entry[0].get('visitors')

        return S / len(data)


    def compute_over18_visitors(self, data):
        """
        Compute the average number of visitors who is over 18
        """

        S = 0

        # For each day
        for day in data:
            # Age part
            age = day.get('age', [])

            # Skip entry concerning persons who are under 18
            eighteens = filter(lambda y: y.get('value') != '12-18', age)
            if len(eighteens) == 0:
                continue


            # Sum number of visitors for each entry
            eighteens = map(lambda y: y.get('visitors', 0), eighteens)
            eighteens = reduce(lambda x, y: x + y, eighteens)

            S += eighteens

        return S / len(data)

    def compute_visitors_by_cities(self, data, all_visitors=1.0):
        """
        Return the average number of visitors by cities
        """

        visitors = {}

        # Collect traffic for each city
        for day in data:
            cities = day.get('cities', [])
            for city in cities:
                city_id = city.get('value', 0)
                visitors[city_id] = visitors.get(city_id, 0) + city.get('visitors')

        for city_id in visitors:
            visitors[city_id] /= len(data) * 1.0
            visitors[city_id] = visitors[city_id] / all_visitors * 100.0

        return visitors

    def compute_visitors_by_countries(self, data, all_visitors=1):
        """
        Return the average number of visitors by countries
        """

        visitors = {}

        # Collect traffic for each country
        for day in data:
            countries = day.get('countries', [])
            for country in countries:
                country_id = country.get('value')
                visitors[country_id] = visitors.get(country_id, 0) + country.get('visitors')

        #
        for country_id in visitors:
            visitors[country_id] /= len(data) * 1.0
            visitors[country_id] = visitors[country_id] / all_visitors * 100

        return visitors

    def extract(self, f):
        """

        Return the computed data

        """
        import sys
        csv.field_size_limit(sys.maxsize)

        reader = csv.reader(f, delimiter=',', quotechar='"')

        for row in reader:
            try:
                gid = int(row[0])
                data = json.loads(row[1])
                data[0]['reach']
            except (KeyError, IndexError, TypeError, ValueError):
                continue

            data = data[:1]

            visitors = self.avg(lambda x: x.get('visitors', 0), data)
            if visitors == 0:
                visitors = 1

            audience = Audience(
                visitors = visitors,
                reach = self.avg(lambda x: x.get('reach', 0), data),
                reach_subscribers = self.avg(lambda x: x.get('reach_subscribers', 0), data),
                views = self.avg(lambda x: x.get('views', 0), data),
                female = self.compute_female_visitors(data) * 100.0 / visitors,
                male = self.compute_male_visitors(data) * 100.0 / visitors,
                over18 = self.compute_over18_visitors(data) * 100.0 / visitors
            )


            analytics = Analytics(
                gid=gid,
                audience = audience,
                countries = self.compute_visitors_by_countries(data, visitors),
                cities = self.compute_visitors_by_cities(data, visitors)
            )

            yield analytics

    def insert(self, analytic):
        try:
            group = models.Group.objects.get(gid=analytic.gid)
        except models.Group.DoesNotExist:
            group = models.Group.objects.create(gid=analytic.gid, name="UNKNOWN!!!", type=1)


        models.Audience.objects.get_or_create(
            group=group,
            visitors=analytic.audience.visitors,
            reach=analytic.audience.reach,
            reach_subscribers=analytic.audience.reach_subscribers,
            views=analytic.audience.views,
            female=analytic.audience.female,
            male=analytic.audience.male,
            over18=analytic.audience.over18
        )

        models.TrafficByCountries.objects.filter(group=group).delete()
        traffic_info = []
        for country_id in analytic.countries.keys():
            traffic_info.append(
                models.TrafficByCountries(group=group, cid=country_id, visitors=analytic.countries[country_id])
            )
        models.TrafficByCountries.objects.bulk_create(traffic_info)

        models.TrafficByCities.objects.filter(group=group).delete()
        traffic_info = []
        for city_id in analytic.cities.keys():
            traffic_info.append(
                models.TrafficByCities(group=group, cid=city_id, visitors=analytic.cities[city_id])
            )
        models.TrafficByCities.objects.bulk_create(traffic_info)


    def handle(self, *args, **kwargs):
        """
        Handle
        """


        f = open(args[0], 'r')

        for entry in self.extract(f):
            self.insert(entry)
