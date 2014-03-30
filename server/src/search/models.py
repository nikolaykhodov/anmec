# -*- coding: utf-8 -*-
from django.db import models


class Group(models.Model):

    GroupType = (
        (1, 'Group'),
        (2, 'Event'),
        (3, 'Public Page')
    )

    class Meta:
        db_table = 'groups'
        index_together = [
            ['type', 'members_count', 'is_closed', 'country', 'city']
        ]

    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=512)

    type = models.IntegerField(choices=GroupType, db_index=True)
    members_count = models.IntegerField(default=0, db_index=True)
    is_closed = models.IntegerField(default=0, db_index=True)
    country = models.IntegerField(default=0, db_index=True)
    city = models.IntegerField(default=0, db_index=True)


class Audience(models.Model):

    group = models.OneToOneField(Group)

    reach = models.IntegerField(default=0, db_index=True)
    reach_subscribers = models.IntegerField(default=0, db_index=True)
    views = models.IntegerField(default=0, db_index=True)
    visitors = models.IntegerField(default=0, db_index=True)
    female = models.FloatField(default=0.0, db_index=True)
    male = models.FloatField(default=0.0, db_index=True)
    over18 = models.FloatField(default=0.0, db_index=True)


class TrafficByCountries(models.Model):

    class Meta:
        index_together = [['cid', 'visitors']]
        unique_together = (('group', 'cid'),)

    group = models.ForeignKey(Group)
    cid = models.IntegerField(default=0, db_index=True)
    visitors = models.FloatField(default=0.0, db_index=True)


class TrafficByCities(models.Model):

    class Meta:
        unique_together = (('group', 'cid'),)
        index_together = [['cid', 'visitors']]

    group = models.ForeignKey(Group)
    cid = models.IntegerField(default=0, db_index=True)
    visitors = models.FloatField(default=0.0, db_index=True)


class Post(models.Model):

    post_id = models.CharField(max_length=32, db_index=True)
    date = models.DateTimeField(db_index=True)
    likes = models.IntegerField(db_index=True)
    reposts = models.IntegerField(db_index=True)
    comments = models.IntegerField(db_index=True)
    repost_like_ratio = models.IntegerField(db_index=True, null=True)

    text = models.TextField(null=True)
    attachments = models.TextField(null=True)
