# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CountryStat.visitors'
        db.alter_column(u'search_countrystat', 'visitors', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'BasicStat.over18'
        db.alter_column(u'search_basicstat', 'over18', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'BasicStat.female'
        db.alter_column(u'search_basicstat', 'female', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'BasicStat.male'
        db.alter_column(u'search_basicstat', 'male', self.gf('django.db.models.fields.FloatField')())

        # Changing field 'CityStat.visitors'
        db.alter_column(u'search_citystat', 'visitors', self.gf('django.db.models.fields.FloatField')())

    def backwards(self, orm):

        # Changing field 'CountryStat.visitors'
        db.alter_column(u'search_countrystat', 'visitors', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'BasicStat.over18'
        db.alter_column(u'search_basicstat', 'over18', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'BasicStat.female'
        db.alter_column(u'search_basicstat', 'female', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'BasicStat.male'
        db.alter_column(u'search_basicstat', 'male', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'CityStat.visitors'
        db.alter_column(u'search_citystat', 'visitors', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'search.basicstat': {
            'Meta': {'object_name': 'BasicStat'},
            'female': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'gid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'over18': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'reach': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'reach_subscribers': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'visitors': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
        },
        u'search.citystat': {
            'Meta': {'object_name': 'CityStat'},
            'cid': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'gid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visitors': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'})
        },
        u'search.countrystat': {
            'Meta': {'object_name': 'CountryStat'},
            'cid': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'gid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visitors': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'})
        },
        u'search.group': {
            'Meta': {'object_name': 'Group', 'db_table': "'groups'"},
            'city': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'country': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'gid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'members_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'type': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['search']