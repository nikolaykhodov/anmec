# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TrafficByCities.gid'
        db.delete_column(u'search_trafficbycities', 'gid_id')

        # Adding field 'TrafficByCities.group'
        db.add_column(u'search_trafficbycities', 'group',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['search.Group']),
                      keep_default=False)

        # Deleting field 'Audience.gid'
        db.delete_column(u'search_audience', 'gid_id')

        # Adding field 'Audience.group'
        db.add_column(u'search_audience', 'group',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['search.Group']),
                      keep_default=False)

        # Deleting field 'TrafficByCountries.gid'
        db.delete_column(u'search_trafficbycountries', 'gid_id')

        # Adding field 'TrafficByCountries.group'
        db.add_column(u'search_trafficbycountries', 'group',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['search.Group']),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'TrafficByCities.gid'
        raise RuntimeError("Cannot reverse this migration. 'TrafficByCities.gid' and its values cannot be restored.")
        # Deleting field 'TrafficByCities.group'
        db.delete_column(u'search_trafficbycities', 'group_id')


        # User chose to not deal with backwards NULL issues for 'Audience.gid'
        raise RuntimeError("Cannot reverse this migration. 'Audience.gid' and its values cannot be restored.")
        # Deleting field 'Audience.group'
        db.delete_column(u'search_audience', 'group_id')


        # User chose to not deal with backwards NULL issues for 'TrafficByCountries.gid'
        raise RuntimeError("Cannot reverse this migration. 'TrafficByCountries.gid' and its values cannot be restored.")
        # Deleting field 'TrafficByCountries.group'
        db.delete_column(u'search_trafficbycountries', 'group_id')


    models = {
        u'search.audience': {
            'Meta': {'object_name': 'Audience'},
            'female': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'male': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'over18': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'reach': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'reach_subscribers': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'visitors': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
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
        },
        u'search.trafficbycities': {
            'Meta': {'object_name': 'TrafficByCities'},
            'cid': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visitors': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'})
        },
        u'search.trafficbycountries': {
            'Meta': {'object_name': 'TrafficByCountries'},
            'cid': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visitors': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'})
        }
    }

    complete_apps = ['search']